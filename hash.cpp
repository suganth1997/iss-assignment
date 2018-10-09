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
	list<char*>* table;

public:
	HashTableImpl(int capacity) {
		size = capacity;
		table = new list<char*>[size];
	} // Constructor. Capacity is the table size for the hash range.
	void insert(int key, char* value) {
		table[key%size].push_back(value);
	}
	char* lookup(int key) {
		auto it = table[key%size].begin();
		return *it;
	}
};
int main(){
	HashTableImpl H(100);
	H.insert(10, "Suganth");
	cout << H.lookup(10) << endl;
	return 0;
}