#include <iostream>
#include <stdio.h>
#include <math.h>
#include <iomanip>

using namespace std;

const int N = 12;

struct Hole {
	double x;
	double y;
};

Hole holes[12] = {
	{ 62.0, 58.4 },
	{ 57.5, 56.0 },
	{ 51.7, 56.0 },
	{ 67.9, 19.6 },
	{ 57.7, 42.1 },
	{ 54.2, 29.1 },
	{ 46.0, 45.1 },
	{ 34.7, 45.1 },
	{45.7, 25.1},
	{34.7, 26.4},
	{28.4, 31.7},
	{33.4, 60.5}
};

double shortestPathLength = DBL_MAX;

int shortestPathOrder[12] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

int next_permutation(const int N, int *P) {
	int s;
	int *first = &P[0];
	int *last = &P[N - 1];
	int *k = last - 1;
	int *l = last;
	//find larges k so that P[k]<P[k+1]
	while (k > first) {
		if (*k < *(k + 1)) {
			break;
		}
		k--;
	}
	//if no P[k]<P[k+1], P is the last permutation in lexicographic order
	if (*k > *(k + 1)) {
		return 0;
	}
	//find largest l so that P[k]<P[l]
	while (l > k) {
		if (*l > *k) {
			break;
		}
		l--;
	}
	//swap P[l] and P[k]
	s = *k;
	*k = *l;
	*l = s;
	//reverse the remaining P[k+1]...P[N-1]
	first = k + 1;
	while (first < last) {
		s = *first;
		*first = *last;
		*last = s;

		first++;
		last--;
	}

	return 1;
}

double dist(Hole a, Hole b) {
	double result = 0;
	result = sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2));
	return result;
}

double calculatePathLength(int P[]) {
	double cnt = 0;
	for (int i = 0; i < N - 1; i++) {
		cnt += dist(holes[P[i] - 1], holes[P[i + 1] - 1]);
	}
	return cnt;
}

void main() {
	int* P = new int[N];

	double curPermLength = 0.0;

	for (int i = 0; i < N; i++) {
		P[i] = i + 1; //holes from 1-8
	}

	do {
		//u nizu P se nalazi jedna permutacija niza od 8 brojeva

		//izracunamo rastojanje izmedju tih rupa
		curPermLength = calculatePathLength(P);

		if (curPermLength < shortestPathLength) {
			shortestPathLength = curPermLength;
			for (int i = 0; i < N; i++) {
				shortestPathOrder[i] = P[i];
			}
		}
	} while (next_permutation(N, P));

	cout << "Najkraca putanja iznosi " << fixed << shortestPathLength << " mm." << endl;
	cout << "Redosled obilaska rupa je: ";
	for (int i = 0; i < N; i++) {
		cout << shortestPathOrder[i];
		if (i < N - 1) {
			cout << " - ";
		}
	}
	cout << endl;

	delete[] P;
}