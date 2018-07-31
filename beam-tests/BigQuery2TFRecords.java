package com.king.kbm;

import com.google.api.services.bigquery.model.TableReference;
import com.google.api.services.bigquery.model.TableRow;
import org.apache.beam.runners.dataflow.options.DataflowPipelineOptions;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.Compression;
import org.apache.beam.sdk.io.TFRecordIO;
import org.apache.beam.sdk.io.gcp.bigquery.BigQueryIO;
import org.apache.beam.sdk.options.*;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.tensorflow.example.BytesList;
import org.tensorflow.example.Example;
import org.tensorflow.example.Feature;
import org.tensorflow.example.Features;
import org.tensorflow.hadoop.shaded.protobuf.ByteString;

import java.io.IOException;
import java.util.Map;
import java.util.Set;


/**
 * This class is used for a Dataflow job which transforms
 * the data in bigquery table to Tfrecords in cloud storage.
 */
public class BigQuery2TFRecords {

    /** command line options interface */
    public interface Options extends DataflowPipelineOptions {
        @Description("Input BigQuery dataset name")
        @Validation.Required
        String getInputBigQueryDataset();
        void setInputBigQueryDataset(String inputBigQueryDataset);

        @Description("Input BigQuery table name")
        @Validation.Required
        String getInputBigQueryTable();
        void setInputBigQueryTable(String inputBigQueryTable);

        @Description("Output Google Cloud Storage path")
        @Validation.Required
        String getOutputGcsFilePath();
        void setOutputGcsFilePath(String outputGcsFilePath);

    }

    public static class CreateExamplesFn extends DoFn<TableRow, byte[]> {

        public CreateExamplesFn() {
        }

        @ProcessElement
        public void processElement(ProcessContext c) throws InterruptedException, IOException {

            Features.Builder featuresBuilder = Features.newBuilder();
            Set<Map.Entry<String, Object>> entries = c.element().entrySet();

            for (Map.Entry<String, Object> entry : entries) {
                String name = entry.getKey();
                if (name.equalsIgnoreCase("kingplayer_id")) {
                    String val = entry.getValue().toString();
                    featuresBuilder.putFeature(name,
                            Feature.newBuilder().setBytesList(
                                    BytesList.newBuilder().addValue(ByteString.copyFromUtf8(val)).build()
                            ).build()
                    );
                    break;
                }
            }

            c.output(Example.newBuilder().setFeatures(featuresBuilder.build()).build().toByteArray());
        }
    }



    public static void main(String[] args) {
        Options options = getOptions(args);

        String projectId = options.getProject();
        String datasetId = options.getInputBigQueryDataset();
        String tableId = options.getInputBigQueryTable();
        String gcsFilePath = options.getOutputGcsFilePath();


        TableReference tableRef = new TableReference().setDatasetId(datasetId).setTableId(tableId);

        Pipeline pipeline = Pipeline.create(options);
        CreateExamplesFn fn = new CreateExamplesFn();

        // Input
        PCollection<TableRow> inputRow = pipeline.apply( "BigQuery-to-TableRow",
                BigQueryIO.readTableRows().from(tableRef));

        // Transform
        PCollection<byte[]> transformed = inputRow.apply("TableRow-to-TfRecords",
                ParDo.of(fn));

        // Output
        transformed.apply("TfRecords-to-Gzip_GCS",
                TFRecordIO.write().to(gcsFilePath).withCompression(Compression.GZIP));

        pipeline.run().waitUntilFinish();
    }

    /**
     * Get command line options
     */
    public static Options getOptions(String[] args) {
        PipelineOptionsFactory.register(Options.class);
        Options options = PipelineOptionsFactory.fromArgs(args)
                .withValidation()
                .as(Options.class);
        return options;
    }

}
