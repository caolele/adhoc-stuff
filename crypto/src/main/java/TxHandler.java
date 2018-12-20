import java.util.ArrayList;
import java.util.HashMap;

public class TxHandler {

    UTXOPool utxoPool;

    /**
     * Creates a public ledger whose current UTXOPool (collection of unspent transaction outputs) is
     * {@code utxoPool}. This should make a copy of utxoPool by using the UTXOPool(UTXOPool uPool)
     * constructor.
     */
    public TxHandler(UTXOPool utxoPool) {
        this.utxoPool = new UTXOPool(utxoPool);
    }

    /**
     * @return true if:
     * (x) all outputs claimed by {@code tx} are in the current UTXO pool,
     * (x) the signatures on each input of {@code tx} are valid,
     * (x) no UTXO is claimed multiple times by {@code tx},
     * (x) all of {@code tx}s output values are non-negative, and
     * (x) the sum of {@code tx}s input values is greater than or equal to the sum of its output
     *     values; and false otherwise.
     */
    public boolean isValidTx(Transaction tx) {
        // a UTXOPool that contains the UTXOs seen so far
        UTXOPool refUtxoPool = new UTXOPool();

        // sum of input and output values
        double sumInputs = 0d;
        double sumOutputs = 0d;

        // Iterate each input
        for (int i = 0; i < tx.numInputs(); i++) {

            Transaction.Input in = tx.getInput(i);
            UTXO utxo = new UTXO(in.prevTxHash, in.outputIndex);
            Transaction.Output out = this.utxoPool.getTxOutput(utxo);

            if (!this.utxoPool.contains(utxo)) {
                return false;
            }
            if (!Crypto.verifySignature(out.address, tx.getRawDataToSign(i), in.signature)) {
                return false;
            }
            sumInputs += out.value;

            // push the current input UTXO
            if (refUtxoPool.contains(utxo)) {
                return false;
            } else {
                refUtxoPool.addUTXO(utxo, out);
            }
        }

        // Iterate each output
        for (Transaction.Output out: tx.getOutputs()) {
            if (out.value < 0) {
                return false;
            } else {
                sumOutputs += out.value;
            }
        }

        return sumInputs >= sumOutputs;
    }

    /**
     * Handles each epoch by receiving an unordered array of proposed transactions, checking each
     * transaction for correctness, returning a mutually valid array of accepted transactions, and
     * updating the current UTXO pool as appropriate.
     */
    public Transaction[] handleTxs(Transaction[] possibleTxs) {
        // Deep copy possibleTxs to keep track of the left-over txs
        HashMap<byte[], Transaction> restTxs = new HashMap<>();
        for (Transaction tx: possibleTxs) {
            tx.finalize();
            restTxs.put(tx.getHash(), tx);
        }

        // Use a list to hold the txs to be returned
        ArrayList<Transaction> result = new ArrayList<>();

        // Loop until no more valid tx
        do {
            // The number of txs before a loop
            int restTxsSize = restTxs.size();

            // One-time Loop
            for (Transaction tx: possibleTxs) {
                if (isValidTx(tx)) {
                    // add to result
                    result.add(tx);
                    // remove UTXO
                    for (Transaction.Input in: tx.getInputs()) {
                        UTXO utxo = new UTXO(in.prevTxHash, in.outputIndex);
                        this.utxoPool.removeUTXO(utxo);
                    }
                    // add UTXO
                    for (int i = 0; i < tx.numOutputs(); i++) {
                        Transaction.Output out = tx.getOutput(i);
                        UTXO utxo = new UTXO(tx.getHash(), i);
                        this.utxoPool.addUTXO(utxo, out);
                    }
                    // remove from restTxs
                    restTxs.remove(tx.getHash());
                }
            }

            // After each complete loop, check for stop condition
            if (restTxsSize == restTxs.size() || restTxs.size() == 0) {
                break;
            }
        } while (true);

        return result.toArray(new Transaction[result.size()]);
    }
}
