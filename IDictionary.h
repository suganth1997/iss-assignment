class IDictionary {
public:
	virtual void insert(int key, char* value) = 0;
	virtual char* lookup(int key) = 0;
};