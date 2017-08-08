#ifndef BANDIT_H
#define BANDIT_H

#include <iostream>
#include <vector>

#include "gsl/gsl_rng.h"
#include "gsl/gsl_randist.h"

using namespace std;

class Bandit{

 private:

  int numArms;
  vector<double> armMeans;
  vector<gsl_rng*> ran;

  double maxMean;

  double cumulativeReward;
  unsigned long int numTotalPulls;


 public:

  Bandit(const int &numArms, const vector<double> &means, const int &seed);
  ~Bandit();

  int getNumArms();
  unsigned long int getNumTotalPulls();

  double pull(const int &armIndex);

  double getCumulativeReward();
  double getRegret();

  void display();
};

#endif

