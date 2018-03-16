vector < vector < int > > threeSum(vector < int > & num) {
  vector < vector < int >> rst;

  if (num.size() < 3) return rst;
  sort(num.begin(), num.end());
  for (int i = 0; i < num.size() - 2; i++) {
    if (i > 0 && num[i] == num[i - 1]) continue;
    for (int j = i + 1, k = num.size() - 1; j < k;) {
      int sum = num[i] + num[j] + num[k];
      if (sum < 0) j++;
      else if (sum > 0) k--;
      else {
        vector < int > curRst;
        curRst.push_back(num[i]);
        curRst.push_back(num[j]);
        curRst.push_back(num[k]);
        rst.push_back(curRst);
        do {
          j++;
        }
        while (num[j] == num[j - 1] && j < k);
        do {
          k--;
        }
        while (num[k] == num[k + 1] && j < k);
      }
    }
  }
  return rst;
}
