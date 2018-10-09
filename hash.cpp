#include <iostream>
#include <list>
using namespace std;

class IDictionary {
	virtual void insert(int key, char* value)=0;
	virtual char* lookup(int key)=0;
};

class HashTableImpl : public IDictionary {
private:
	int size;
	list<pair<int, char*>>* table;

public:
	HashTableImpl(int capacity) {
		size = capacity;
		table = new list<pair<int, char*>>[size];
	} // Constructor. Capacity is the table size for the hash range.
	void insert(int key, char* value) {
		table[key%size].push_back(make_pair(key, value));
	}
	char* lookup(int key) {
		auto it = table[key%size].begin();
		for(; it != table[key%size].end(); it++)
			if((*it).first == key) return (*it).second;
		return NULL;
	}
};
int main(){
	HashTableImpl H(100);
	H.insert(10, (char*)"Suganth");
	H.insert(110, (char*)"Ilangovan");
	cout << H.lookup(10) << endl << H.lookup(11) << endl;
	return 0;
}