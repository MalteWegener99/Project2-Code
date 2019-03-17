#include <stdio.h>
#include <math.h>

const double f = 1 / 298.257223563;
const double e_2 = 2.0 * f - f*f;
const double a = 6378137.0;  //SMA

double* xyz2llh(double* pos){
    //[phi, lambda, h]
    double x = pos[0];
    double y = pos[1];
    double z = pos[2];
    double lam = atan(y/x);

    double p = sqrt(x*x + y*y);

    //inital calculation
    double phi = atan(z/((1-e_2) * p));
    double h = 0.;

    for(unsigned int i = 0; i < 10; i++){
        double N = a/(sqrt(1-e_2*pow(sin(phi),2)));
        h = p/(cos(phi)) - N;
        double denom = 1-e_2*N/(N+h);
        phi = atan(z/(denom*p));
    }
    double* arr = new double[3]{phi, lam, h};
    return arr;
}