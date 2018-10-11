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
		return (char*)"";
	}
};



class ArrayDictImpl : public IDictionary {
private:
	int size = 0;
	int total_capacity;
    pair<int, char*>* table;

public:
	ArrayDictImpl(int capacity) {
		table = new pair<int, char*>[capacity];
		total_capacity = capacity;
	}

	void insert(int key, char* value) {
        if(size == total_capacity) throw out_of_range("Number of inserts exceeds capacity");
		table[size].first = key;
        table[size].second = value;
		size++;
	}

	char* lookup(int key) {
		for (int i = 0; i < size; i++)
			if (table[i].first == key) return table[i].second;
		return (char*)"";
	}
};

int compare_function(const void* x, const void* y) {
	auto a = *((pair<int, char*>*)x);
	auto b = *((pair<int, char*>*)y);
	return a.first - b.first;
}

class BSearchDictImpl : public IDictionary {
private:
	pair<int,char*>* table;
	int size = 0;
	int total_size;
public:
	BSearchDictImpl(int capacity) {
		total_size = capacity;
		table = new pair<int,char*>[capacity];
	}
	
	void insert(int key, char* value){
        if(size == total_size) throw out_of_range("Number of inserts exceeds capacity");
		table[size].first = key;
		table[size].second = value;
		size++;
		if(size == total_size) sort();
	}
	void debug(){
		for(int i=0; i<size; i++){
			cout << table[i].first << " ";
		}
		cout << endl;
	}
	void sort(){
		qsort(table, size, sizeof(pair<int, char*>), compare_function);
	}
	
	char* lookup(int key){
		int a = 0, b = size;
		while(a <= b){
			int n = a + (b-a)/2;
			if(table[n].first == key) return table[n].second;
			else if(table[n].first > key) b = n - 1;
			else a = n + 1;
		}
		return (char*)"";
	}
};
/*
char* get_cha(int i) {
	auto s = new string;
	*s = "Hey Bro " + to_string(i);
	//cout << &s[0] << endl;
	return &(*s)[0];
}
*/

