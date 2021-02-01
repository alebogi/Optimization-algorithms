#include <iostream>
#include <time.h>
#include <iomanip>

using namespace std;

unsigned long long int cnt = 0; //broji pozive funkcije fun

bool fun(int x1, int x2, int x3, int x4) {
	cnt++;
	if ( (x1 + x2 + x3 + x4 == 711) && (x1 * x2 * x3 * x4 == 711000000) )
		return true;
	else 
		return false;
}

/**
* Program pronalazi cene koje odgovaraju uslovu: a+b+c+d = a*b*c*d = 7.11
* Program je optimizovan. Prvobitni program je sadrzao 4 for petlje koje su isle od 1 do 708.
* Od 1 zato sto cena ne moze da bude ==0, a do 708 zato sto max cena moze da bude 708 (1+1+1+708=711)
* Takav program pronalazi sve permutacije resenja i izvrsava se dosta dugo. Posto nema potrebe za pronalazenjem svih mogucih
* permutacija 4 broja, program je izmenjen.
*/


int main(){
	time_t startTime;
	time(&startTime);

	int x1, x2, x3, x4;
	for (x1 = 1; x1 <= 708; x1++) {
		for (x2 = x1; x2 <= 708 - x1; x2++) {
			for (x3 = x2; x3 <= 708 - x2; x3++) {
				for (x4 = x3; x4 <= 708 - x3; x4++) {
					if (fun(x1, x2, x3, x4)) {
						cout << setprecision(2) << fixed << "Cene su: " << (float)x1 / 100 << "$, " << (float)x2 / 100 
							<< "$, " << (float)x3 / 100 << "$, " << (float)x4 / 100 << "$" << endl;
					}
				}
			}
		}
	}

	time_t endTime;
	time(&endTime);
	
	cout << "Vreme izvrsavanja programa: " << endTime - startTime << " sekundi." << endl;
	cout << "Funkcija se pozivala " << cnt << "puta." << endl;
	
//	cin.get();
	return 0;
}




