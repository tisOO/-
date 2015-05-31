#include <iostream>
#include <map>
#include <string>
#include <fstream>
#include <chrono>

// 32битная хеш-функция
unsigned int HashH37(const char * str)
{
	unsigned int hash = 2139062143;
	for(; *str; str++)
		hash = 37 * hash + *str;
	return hash;
}


// атака на коллизии
void generation(std::map<int, std::string> &hashes) {
	std::string buf;
	for (int i = 0; i < 3; ++i) {
		buf.push_back(char(-127));
	}
	int pos = buf.length()-1;
	int collision = 0;
	while (hashes.size() < 65536) {
		if ( buf[pos] == 127) {
			int b_pos = pos;
			while (buf[b_pos] == 127 && b_pos >= 0) {
				buf[b_pos] = char(-127);
				b_pos -= 1;
			}
			buf[b_pos] = char((int(buf[b_pos]) + 1));;
		}
		buf[pos] = char((int(buf[pos]) + 1));
		int hash = HashH37(buf.c_str());
		if (hashes.find(hash) != hashes.end()) {
			++collision;
		}
		hashes[hash] = buf;
		
	}
	std::cout <<"Collisions: " << collision << std::endl;
}

// полная атака
void generation_full(std::map<int, std::string> &hashes) {
	std::string buf;
	for (int j = 0; j < 12; ++j) {
		buf.push_back(char(-127));
	}
	int pos = buf.length()-1;
	unsigned long long int collision = 0;
	while (hashes.size() < 2147483648) {
		/*if ( hashes.size() % 42946 == 0 ) {
			std::cout << hashes.size() << std::endl;
		}*/
		if ( buf[pos] == 127) {
			int b_pos = pos;
			while (buf[b_pos] == 127 && b_pos >= 0) {
				buf[b_pos] = char(-127);
				b_pos -= 1;
			}
			buf[b_pos] = char((int(buf[b_pos]) + 1));;
		}
		buf[pos] = char((int(buf[pos]) + 1));
		int hash = HashH37(buf.c_str());
		if (hashes.find(hash) != hashes.end()) {
			++collision;
		}
		hashes[hash] = buf;
	}
	std::cout <<"Collisions: " << collision << std::endl;
}

void test1() {
	std::map<int, std::string> hashes;
	std::cout << "Start generation" << std::endl;
	auto start = std::chrono::steady_clock::now();
	generation_full(hashes);
	auto stop = std::chrono::steady_clock::now();
	std::cout << "Finish generation" << std::endl;
	std::cout <<"Generation time" << std::endl;
	std::cout << "hours:" << std::chrono::duration_cast<std::chrono::hours>(stop - start).count() << std::endl
		<< "minutes:" << std::chrono::duration_cast<std::chrono::minutes>(stop - start).count() % 60 << std::endl
		<< "seconds:" << std::chrono::duration_cast<std::chrono::seconds>(stop - start).count() % 60 << std::endl
		<< "milliseconds:" << std::chrono::duration_cast<std::chrono::milliseconds>(stop - start).count() % 1000 << std::endl
		<< "microseconds:" << std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count() % 1000 << std::endl
		<< "nanoseconds:" << std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start).count() % 1000 << std::endl;
	
	std::ifstream fin("english.txt");	
	std::string pswd;
	unsigned int collision = 0;
	unsigned int not_found = 0;
	std::cout << "Start testing on the dictionary" << std::endl;
	char buf[100];
	start = std::chrono::steady_clock::now();
	while (fin.getline(buf, 100)) {

		int hash = HashH37(buf);
		if (hashes.find(hash) != hashes.end()) {
			++collision;
		} else {
			++not_found;
		}
	}
	stop = std::chrono::steady_clock::now();
	std::cout << "Finished" << std::endl;
	std::cout <<"Dictionary test time" << std::endl;
	std::cout << "hours:" << std::chrono::duration_cast<std::chrono::hours>(stop - start).count() << std::endl
		<< "minutes:" << std::chrono::duration_cast<std::chrono::minutes>(stop - start).count() % 60 << std::endl
		<< "seconds:" << std::chrono::duration_cast<std::chrono::seconds>(stop - start).count() % 60 << std::endl
		<< "milliseconds:" << std::chrono::duration_cast<std::chrono::milliseconds>(stop - start).count() % 1000 << std::endl
		<< "microseconds:" << std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count() % 1000 << std::endl
		<< "nanoseconds:" << std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start).count() % 1000 << std::endl;
	
	std::cout << "Collisions:" << collision << std::endl;
	std::cout << "Not found:" << not_found << std::endl;
}

void test2() {
	std::map<int, std::string> hashes;
	std::ifstream fin("english.txt");	
	std::string pswd;
	unsigned int collision = 0;
	unsigned int not_found = 0;
	std::cout << "Start testing on the dictionary" << std::endl;
	char buf[100];
	auto start = std::chrono::steady_clock::now();
	while (fin.getline(buf, 100)) {

		int hash = HashH37(buf);
		if (hashes.find(hash) != hashes.end()) {
			++collision;
		} else {
			hashes[hash] = buf;
			++not_found;
		}
	}
	auto stop = std::chrono::steady_clock::now();
	std::cout << "Finished" << std::endl;
	std::cout <<"Dictionary test time" << std::endl;
	std::cout << "hours:" << std::chrono::duration_cast<std::chrono::hours>(stop - start).count() << std::endl
		<< "minutes:" << std::chrono::duration_cast<std::chrono::minutes>(stop - start).count() % 60 << std::endl
		<< "seconds:" << std::chrono::duration_cast<std::chrono::seconds>(stop - start).count() % 60 << std::endl
		<< "milliseconds:" << std::chrono::duration_cast<std::chrono::milliseconds>(stop - start).count() % 1000 << std::endl
		<< "microseconds:" << std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count() % 1000 << std::endl
		<< "nanoseconds:" << std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start).count() % 1000 << std::endl;
	
	std::cout << "Collisions:" << collision << std::endl;
	std::cout << "Original:" << not_found << std::endl;

}


int main() {
	test1();
	return 0;
}