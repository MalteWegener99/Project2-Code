#include <stdio.h>
#include <math.h>
#include <stdint.h>
#include <vector>
#include <string>
#include <fstream>

// Cosntants for WGS84
const double f = 1 / 298.257223563;
const double e_2 = 2.0 * f - f*f;
const double a = 6378137.0;  //SMA

double* xyz2llh(double*);

class Sample{
public:
    int64_t time;
    double pos[3];
    double mat[9];
    void convert();
};

void Sample::convert(){
    double* converted = xyz2llh(pos);
    for(int i = 0; i < 3; i++){
        pos[i] = converted[i];
    }
}

typedef std::vector<Sample> t_collection;

t_collection load_from_binary_file(char* path){
    std::ifstream file;
    file.open(path, std::ios::in | std::ios::binary);

    t_collection Collector;
    Collector.reserve(6000);
    int i = 0;
    while(!file.eof()){
        i++;
        //time
        char time_bin[8];
        file.read(time_bin, 8);
        int64_t time = *(int64_t*)time_bin;
        //numbers
        char numbers_bin[8*(9+3)];
        file.read(numbers_bin, 8*(9+3));
        double* numbers = (double*)numbers_bin;
        Sample smp;
        smp.time = time;
        smp.pos[0] = numbers[0];
        smp.pos[1] = numbers[1];
        smp.pos[2] = numbers[2];

        for(int i = 0; i < 9; i++){
            smp.mat[i] = numbers[i+2];
        }
        Collector.push_back(smp);
        printf("%d\n", i);
    }
    file.close();

    return Collector;
}

void save_to_binary_file(t_collection Collection, char* path){
    std::ofstream file;
    file.open(path, std::ios::out | std::ios::binary | std::ios::trunc);

    for(int i = 0; i < Collection.size(); i++){
        file.write((char*)Collection[i].time, 8*13);
    }
    file.close();
}


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

int main(int argc, char* argv[]){
    if(argc < 3){
        printf("give at least 2 Arguments");
        return 1;
    }
    else if(argc > 3){
        printf("too many arguments");
        return 1;
    }
    t_collection Collection = load_from_binary_file(argv[1]);
    for(int i = 0; i < Collection.size(); i++){
        Collection[i].convert();
    }
    printf("%zu\n", Collection.size());
    save_to_binary_file(Collection, argv[2]);
}