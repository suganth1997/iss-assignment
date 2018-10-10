#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <ctime>
#include <fstream>
using namespace std;
void gen_random(char *s, const int len) {
	for (int i = 0; i < len; ++i) {
		int randomChar = rand() % (26 + 26 + 10);
		if (randomChar < 26)
			s[i] = 'a' + randomChar;
		else if (randomChar < 26 + 26)
			s[i] = 'A' + randomChar - 26;
		else
			s[i] = '0' + randomChar - 26 - 26;
	}
	s[len] = 0;
}

int main(int argc, char** argv) {
	srand(time(NULL));
	vector<int> v;
	vector<char*> vs;
	for (int i = 0; i < stoi(argv[1]); i++) {
		char* str;
		v.push_back(i);
		gen_random(str, rand() % 20);
		vs.push_back(str);
	}
	ofstream file;
	file.open(argv[2]);
	file << stoi(argv[1]) << endl;
	random_shuffle(v.begin(), v.end());
	for (int i = 0; i < v.size(); i++)
		file << v[i] << "\t" << vs[i] << endl;

	file.close();
	return 0;
}