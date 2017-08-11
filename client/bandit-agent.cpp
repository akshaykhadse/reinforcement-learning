#include <iostream>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <math.h>
#include <vector>
#include <random>
#include <string>

#include "gsl/gsl_rng.h"
#include "gsl/gsl_randist.h"

#define MAXHOSTNAME 256

using namespace std;

void options(){

  cout << "Usage:\n";
  cout << "bandit-agent\n";
  cout << "\t[--numArms numArms]\n";
  cout << "\t[--randomSeed randomSeed]\n";
  cout << "\t[--horizon horizon]\n";
  cout << "\t[--hostname hostname]\n";
  cout << "\t[--port port]\n";
  cout << "\t[--algorithm algorithm]\n";
  cout << "\t[--epsilon epsilon]\n";

}

/*
  Read command line arguments, and set the ones that are passed (the others remain default.)
*/
bool setRunParameters(int argc, char *argv[], int &numArms, int &randomSeed, unsigned long int &horizon, string &hostname, int &port, string &algorithm, double &epsilon){

  int ctr = 1;
  while(ctr < argc){

    //cout << string(argv[ctr]) << "\n";

    if(string(argv[ctr]) == "--help"){
      return false;//This should print options and exit.
    }
    else if(string(argv[ctr]) == "--numArms"){
      if(ctr == (argc - 1)){
	return false;
      }
      numArms = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--randomSeed"){
      if(ctr == (argc - 1)){
	return false;
      }
      randomSeed = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--horizon"){
      if(ctr == (argc - 1)){
	return false;
      }
      horizon = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--hostname"){
      if(ctr == (argc - 1)){
	return false;
      }
      hostname = string(argv[ctr + 1]);
      ctr++;
    }
    else if(string(argv[ctr]) == "--port"){
      if(ctr == (argc - 1)){
	return false;
      }
      port = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--algorithm"){
      if(ctr == (argc - 1)){
  return false;
      }
      algorithm = string(argv[ctr + 1]);
      ctr++;
    }
     else if(string(argv[ctr]) == "--epsilon"){
      if(ctr == (argc - 1)){
  return false;
      }
      epsilon = atof(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else{
      return false;
    }

    ctr++;
  }

  return true;
}

/* ============================================================================= */
/* Write your algorithms here */

int getIndexOfLargestElement(double arr[], int size) {
    int largestIndex = 0;
    for (int index = largestIndex; index < size; index++) {
        if (arr[largestIndex] < arr[index]) {
            largestIndex = index;
        }
    }
    return largestIndex;
}

int *pullsDone;
float *rewardsGot;
double *eMean;
double *ucb;
double *qMax;
double *beta;
gsl_rng * r;  // pointer to a global random no generator

void eMeanUpdate(float reward, int pArmPulled){
  rewardsGot[pArmPulled] += reward;
  pullsDone[pArmPulled] += 1;
  eMean[pArmPulled] = (double)rewardsGot[pArmPulled] / (double)pullsDone[pArmPulled];
}

void ucbUpdate(float reward, int pulls, int pArmPulled){
  eMeanUpdate(reward, pArmPulled);
  ucb[pArmPulled] = (double)eMean[pArmPulled] + sqrt((double)2.0*(log(pulls))/(double)pullsDone[pArmPulled]);
  //cout << sqrt(2.0*(float)(log(pulls))/(float)pullsDone[pArmPulled]) << endl;
}

void updateQMax(float reward, int pulls, int numArms, int pArmPulled){
  eMeanUpdate(reward, pArmPulled);
  double delta = 1e-8;
  double epsilon = 1e-10;
  for(int i=0; i<numArms; i++){
    bool converged = false;
    double p = max((double)eMean[i], delta);
    double q = p + delta;
    for(int j=0;(j<100&&!converged);++j){
      double kl = p * log(p/q) + (1-p)*log((1-p)/(1-q));
      double dkl = (q-p)/(q*(1.0-q));
      double f  = log(pulls)/(double)pullsDone[i] - kl;
      double df = - dkl;
      if(f*f < epsilon){
        converged=true;
        break;
      }
      q = min(1-delta, max(q-f/df, p+delta));
    }
    if(!converged){
      //cout << "WARNING:Newton iteration in KL-UCB algorithm did not converge!!" << endl;
    }
    qMax[i] = q;
  }
}

int sampleArm(string algorithm, double epsilon, int pulls, float reward, int numArms, int pArmPulled = 0){
  if(algorithm.compare("rr") == 0){
    return(pulls % numArms);
  }
  else if(algorithm.compare("epsilon-greedy") == 0){
    int rNum = rand() % 100;

    if(pulls == 0){
      pullsDone = new int[numArms];
      rewardsGot = new float[numArms];
      eMean = new double[numArms];
      for(int i=0; i<numArms; i++){
        pullsDone[i] = 0;
        rewardsGot[i] = 0.0;
        eMean[i] = (double)0;
      }
      return rNum % numArms;
    }else{
      eMeanUpdate(reward, pArmPulled);
      if(rNum > (int)((float)epsilon*100.0)){
        return getIndexOfLargestElement(eMean, numArms);
      }else{
        return rNum % numArms;
      }
    }
  }
  else if(algorithm.compare("UCB") == 0){
    if(pulls == 0){
      pullsDone = new int[numArms];
      rewardsGot = new float[numArms];
      eMean = new double[numArms];
      ucb = new double[numArms];
      for(int i=0; i<numArms; i++){
        pullsDone[i] = 0;
        rewardsGot[i] = 0.0;
        eMean[i] = (double)0;
        ucb[i] = (double)0;
      }
      return pulls % numArms;
    }else{
      ucbUpdate(reward, pulls, pArmPulled);
      if(pulls < numArms){
        return pulls % numArms;
      }else{
        return getIndexOfLargestElement(ucb, numArms);
      }
    }
  }
  else if(algorithm.compare("KL-UCB") == 0){
    if(pulls == 0){
      pullsDone = new int[numArms];
      rewardsGot = new float[numArms];
      eMean = new double[numArms];
      qMax = new double[numArms];
      for(int i=0; i<numArms; i++){
        pullsDone[i] = 0;
        rewardsGot[i] = 0.0;
        eMean[i] = (double)0;
        qMax[i] = (double)0;
      }
      return pulls % numArms;
    }else{
      updateQMax(reward, pulls, numArms, pArmPulled);
      if(pulls < numArms){
        return pulls % numArms;
      }else{
        return getIndexOfLargestElement(qMax, numArms);
      }
    }
  }
  else if(algorithm.compare("Thompson-Sampling") == 0){
    if(pulls == 0){
      pullsDone = new int[numArms];
      rewardsGot = new float[numArms];
      eMean = new double[numArms];
      beta = new double[numArms];
      for(int i=0; i<numArms; i++){
        pullsDone[i] = 0;
        rewardsGot[i] = 0.0;
        eMean[i] = (double)0;
        beta[i] = (double)0;
      }
    }
    eMeanUpdate(reward, pArmPulled);
    for(int i=0; i<numArms; i++){
      beta[i] = gsl_ran_beta (r, rewardsGot[i] + 1.0, (float)pullsDone[i] - rewardsGot[i] + 1.0);
    }
    return getIndexOfLargestElement(beta, numArms);
    }
  else{
    return -1;
  }
}

void deleteArrays(string algorithm){
    if(algorithm.compare("epsilon-greedy") == 0){
        delete[]pullsDone;
        delete[]rewardsGot;
        delete[]eMean;
    }
    else if(algorithm.compare("UCB") == 0){
        delete[]pullsDone;
        delete[]rewardsGot;
        delete[]eMean;
        delete[]ucb;
    }
    else if(algorithm.compare("Thompson-Sampling") == 0){
        delete[]pullsDone;
        delete[]rewardsGot;
        delete[]eMean;
        delete[]beta;
    }    
}

/* ============================================================================= */


int main(int argc, char *argv[]){
  // Run Parameter defaults.
  int numArms = 5;
  int randomSeed = time(0);
  unsigned long int horizon = 200;
  string hostname = "localhost";
  int port = 5000;
  string algorithm="random";
  double epsilon=0.0;
  srand(randomSeed);
  
  // have to do these things first - they are explained in manual
  const gsl_rng_type * T;
  gsl_rng_env_setup();
  T = gsl_rng_default;
  r = gsl_rng_alloc (T);
  gsl_rng_set (r, time(0));

  //Set from command line, if any.
  if(!(setRunParameters(argc, argv, numArms, randomSeed, horizon, hostname, port, algorithm, epsilon))){
    //Error parsing command line.
    options();
    return 1;
  }

  struct sockaddr_in remoteSocketInfo;
  struct hostent *hPtr;
  int socketHandle;

  bzero(&remoteSocketInfo, sizeof(sockaddr_in));

  if((hPtr = gethostbyname((char*)(hostname.c_str()))) == NULL){
    cerr << "System DNS name resolution not configured properly." << "\n";
    cerr << "Error number: " << ECONNREFUSED << "\n";
    exit(EXIT_FAILURE);
  }

  if((socketHandle = socket(AF_INET, SOCK_STREAM, 0)) < 0){
    close(socketHandle);
    exit(EXIT_FAILURE);
  }

  memcpy((char *)&remoteSocketInfo.sin_addr, hPtr->h_addr, hPtr->h_length);
  remoteSocketInfo.sin_family = AF_INET;
  remoteSocketInfo.sin_port = htons((u_short)port);

  if(connect(socketHandle, (struct sockaddr *)&remoteSocketInfo, sizeof(sockaddr_in)) < 0){
    //code added
    cout<<"connection problem"<<".\n";
    close(socketHandle);
    exit(EXIT_FAILURE);
  }


  char sendBuf[256];
  char recvBuf[256];

  float reward = 0;
  unsigned long int pulls=0;
  int armToPull = sampleArm(algorithm, epsilon, pulls, reward, numArms);

  sprintf(sendBuf, "%d", armToPull);

  //cout << "Sending action " << armToPull << ".\n";
  while(send(socketHandle, sendBuf, strlen(sendBuf)+1, MSG_NOSIGNAL) >= 0){

    char temp;
    recv(socketHandle, recvBuf, 256, 0);
    sscanf(recvBuf, "%f %c %lu", &reward, &temp, &pulls);
    //cout << "Received reward " << reward << ".\n";
    //cout<<"Num of  pulls "<<pulls<<".\n";
    cout << reward << endl;

    //epsilon *= 0.95;
    armToPull = sampleArm(algorithm, epsilon, pulls, reward, numArms, armToPull);

    sprintf(sendBuf, "%d", armToPull);
    //cout << "Sending action " << armToPull << ".\n";
  }

  close(socketHandle);
  
  // at end of program must get rid of memory used by the generator
  gsl_rng_free (r);

  deleteArrays(algorithm);

  //cout << "Terminating.\n";

  return 0;
}
