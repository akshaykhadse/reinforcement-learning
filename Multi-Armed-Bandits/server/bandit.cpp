#include "bandit.h"

Bandit::Bandit(const int &numArms, const vector<double> &means, const int &seed){
  
  this->numArms = numArms;

  armMeans.clear();
  maxMean = -1.0;
  for(int a = 0; a < numArms; a++){
    armMeans.push_back(means[a]);
    if(armMeans[a] > maxMean){
      maxMean = armMeans[a];
    }
  }

  gsl_rng* seedGenerator = gsl_rng_alloc(gsl_rng_mt19937);
  gsl_rng_set(seedGenerator, seed);

  ran.clear();
  for(int a = 0; a < numArms; a++){
    ran.push_back(gsl_rng_alloc(gsl_rng_mt19937));
    gsl_rng_set(ran[a], gsl_rng_get(seedGenerator));
  }

  gsl_rng_free(seedGenerator);

  cumulativeReward = 0;
  numTotalPulls = 0;
}


Bandit::~Bandit(){
  
  for(int a = 0; a < numArms; a++){
    gsl_rng_free(ran[a]);
  }
}
 
int Bandit::getNumArms(){

  return numArms;
}

unsigned long int Bandit::getNumTotalPulls(){

  return numTotalPulls;
}


double Bandit::pull(const int &armIndex){

  double reward = 0;
  if(gsl_rng_uniform(ran[armIndex]) < armMeans[armIndex]){
    reward = 1.0;
  }

  cumulativeReward += reward;
  numTotalPulls++;

  return reward;
}


double Bandit::getCumulativeReward(){

  return cumulativeReward;
}

double Bandit::getRegret(){

  return ((numTotalPulls * maxMean) - cumulativeReward);
}

void Bandit::display(){

  cout << "********************************\n";
  for(int a = 0; a < numArms; a++){
    cout << a << ": " << armMeans[a] << "\n";
  }

  cout << "max mean: " << maxMean << "\n";
  cout << "********************************\n";
}

