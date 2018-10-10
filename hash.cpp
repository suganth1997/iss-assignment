#include <iostream>
#include <vector>
#include <list>
#include <string>
#include <algorithm>
#include "IDictionary.h"
using namespace std;


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



class ArrayDictImpl : public IDictionary {
private:
	int size = 0;
	int total_capacity;
	int* keys;
	char** values;

public:
	ArrayDictImpl(int capacity) {
		keys = new int[capacity];
		values = new char*[capacity];
		total_capacity = capacity;
	}

	void insert(int key, char* value) {
		keys[size] = key;
		values[size] = value;
		size++;
	}

	char* lookup(int key) {
		for (int i = 0; i < size; i++)
			if (keys[i] == key) return values[i];
		return NULL;
	}
};

int compare_function(const void* x, const void* y) {
	auto a = *((pair<int, char*>*)x);
	auto b = *((pair<int, char*>*)y);
	return a.first - b.first;
}
class BSearchDictImpl : public IDictionary {
private:
	vector<pair<int, char*>> b_hash;
	int size = 0;
	int total_size;
public:
	BSearchDictImpl(int capacity) {
		total_size = capacity;
	}

	/*
	void sort() {
		qsort(&b_hash[0], b_hash.size(), sizeof(pair<int, char*>), compare_function);
	}

	void insert(int key, char* value) {
		b_hash.push_back(make_pair(key, value));
		size++;
		if (size == total_size) sort();
	}

	void debug() {
		for (int i = 0; i < total_size; i++)
			cout << b_hash[i].first << "\t" << b_hash[i].second << endl;
	}
	char* lookup(int key) {
		int a = 0, b = total_size;
		//debug();
		while (a < b) {
			int n = a + (b - a) / 2;
			if (b_hash[n].first == key) return b_hash[n].second;
			else if (b_hash[n].first > key) b = n;
			else a = n;
		}
		return NULL;
	}
	*/
};

char* get_cha(int i) {
	string s = "Hey" + to_string(i);
	cout << &s[0] << endl;
	return &s[0];
}

int main(){
	IDictionary* H = new BSearchDictImpl(10);
	for (int i = 0; i < 10; i++)
		H->insert(i, get_cha(i));
	cout << H->lookup(1) << endl;

	return 0;
}