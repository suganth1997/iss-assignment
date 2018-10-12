#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <sstream>
#include <vector>
#include <ctime>
#include "DictImpl.cpp"
using namespace std;
int insert_count, lookup_count;
double insert_time, lookup_time = 0;

int parseLine(char* line){
    // This assumes that a digit will be found and the line ends in " Kb".
    int i = strlen(line);
    const char* p = line;
    while (*p <'0' || *p > '9') p++;
    line[i-3] = '\0';
    i = atoi(p);
    return i;
}
int getValue(){ //Note: this value is in KB!
    FILE* file = fopen("/proc/self/status", "r");
    int result = -1;
    char line[128];

    while (fgets(line, 128, file) != NULL){
        if (strncmp(line, "VmRSS:", 6) == 0){
            result = parseLine(line);
            break;
        }
    }
    fclose(file);
    return result;
}

double time_taken(struct timespec start, struct timespec end){
    if(start.tv_sec == end.tv_sec)
      return (end.tv_nsec - start.tv_nsec)/1000000.0;
    else
      return double((end.tv_sec - start.tv_sec)*1e3 + (end.tv_nsec - start.tv_nsec)/double(1e6));
}

void Load_Dict(IDictionary* dict, char* insert_file){
    ifstream file;
    file.open(insert_file);
    string line;
    int count = 0;
    struct timespec start, end;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    while(getline(file, line)){
        stringstream ss(line);
        int k;
        string full, word;
        ss >> k;
        ss >> full;
        while(ss >> word) full += " " + word;
        string* v = new string;
        *v = full;
        dict -> insert(k,&(*v)[0]);
        count++;
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    insert_count = count;
    insert_time = time_taken(start, end);
}

void Lookup_Dict(IDictionary* dict, char* lookup_file, char* output_file){
    ifstream file;
    file.open(lookup_file);
    int key;
    int count = 0;
    vector<int> keys;
    vector<char*> results;
    while(file >> key){
        keys.push_back(key);
    }
    file.close();
    
    
    struct timespec start, end;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    for(auto it = keys.begin(); it != keys.end(); it++){
        char* ans = dict -> lookup(*it);
        results.push_back(ans);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    lookup_time = time_taken(start, end);
    
    
    ofstream out;
    out.open(output_file);
    auto itk = keys.begin();
    for(auto it = results.begin(); it != results.end(); it++){
        out << *itk << "\t" << (*it) << endl;
        itk++;
        count++;
    }
    lookup_count = count;
}

int main(int argc, char** argv){
    IDictionary* dict;
    
    if(strcmp("hash", argv[1]) == 0)
        dict = new HashTableImpl(stoi(argv[2]));
    
    else if(strcmp("array", argv[1]) == 0)
        dict = new ArrayDictImpl(stoi(argv[2]));
    
    else if(strcmp("bsearch", argv[1]) == 0)
        dict = new BSearchDictImpl(stoi(argv[2]));
    
    else{
        cout << "Invalid command line arguments" << endl;
        return 0;
    }
    
    Load_Dict(dict, argv[3]);
    Lookup_Dict(dict, argv[4], argv[5]);
    
    cout << argv[1] << "," << insert_count << "," << insert_time << "," << lookup_count << "," << lookup_time << endl;
    cout << "Memory used = " << getValue() << " kb" << endl << endl;
    return 0;
}
