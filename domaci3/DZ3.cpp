#include <iostream>
#include <stdio.h>

using namespace std;

int cenePovezivanja[10][10] = {
	{ 0,374,200,223,108,178,252,285,240,356 },
{ 374,0,255,166,433,199,135,95,136,17 },
{ 200,255,0,128,277,821,180,160,131,247 },
{ 223,166,128,0,430,47,52,84,40,155 },
{ 108,433,277,430,0,453,478,344,389,423 },
{ 178,199,821,47,453,0,91,110,64,181 },
{ 252,135,180,52,478,91,0,114,83,117 },
{ 285,95,160,84,344,110,114,0,47,78 },
{ 240,136,131,40,389,64,83,47,0,118 },
{ 356,17,247,155,423,181,117,78,118,0 }
};

int n = 10;
int k = 8; //varijacije: n-2

int cena = 0;
int minCena = INT_MAX;

void SequenceToSpanningTree(int* P, int* T) {
	int i, j, q = 0;
	int* V = new int[n];

	for (i = 0; i < n; i++) {
		V[i] = 0;
	}

	for (i = 0; i < k; i++) {
		V[P[i] - 1] += 1;
	}

	for (i = 0; i < k; i++) {
		for (j = 0; j < n; j++) {
			if (V[j] == 0) {
				V[j] = -1;
				T[q++] = j + 1;
				T[q++] = P[i];
				V[P[i] - 1]--;
				break;
			}
		}
	}

	j = 0;
	for (i = 0; i < n; i++) {
		if (V[i] == 0 && j == 0) {
			T[q++] = i + 1;
			j++;
		}
		else if (V[i] == 0 && j == 1) {
			T[q++] = i + 1;
			break;
		}
	}

	delete[] V;
}

void variations_with_repetition(int* najboljeGrane) {
	int graneLength = 2 * (k + 1);
	int penali[10];
	int* pamtig = new int[2 * (k + 1)];
	int q;
	int* P = new int[k];
	int* pomP = new int[k];

	for (int i = 0; i < k; i++) {
		P[i] = 0;
	}



	do {
		cena = 0;

		for (int i = 0; i < n; i++)
			penali[i] = 0;

		for (int i = 0; i < k; i++)
			pomP[i] = P[i] + 1;
		//zelimo 1-10, zato +1

		SequenceToSpanningTree(pomP, pamtig);


		for (int i = 0; i < 2 * (k + 1); i += 2) {
			cena += cenePovezivanja[pamtig[i] - 1][pamtig[i + 1] - 1];
		}

		for (int i = 0; i < graneLength; i++) {
			penali[pamtig[i] - 1]++;
		}


		for (int i = 0; i < n; i++) {
			if (penali[i] >= 4)
				cena += (100 * (penali[i] - 3));
		}

		if (cena < minCena) {
			minCena = cena;
			for (int i = 0; i < 2 * (k + 1); i++)
				najboljeGrane[i] = pamtig[i];
		}



		q = k - 1;
		while (q >= 0) {
			P[q]++;
			if (P[q] == n) {
				P[q] = 0;
				q--;
			}
			else {
				break;
			}
		}
	} while (q >= 0);

	delete[] P;
}

int main() {
	int graneLength = 2 * (k + 1);
	int* najboljeGrane = new int[graneLength];

	variations_with_repetition(najboljeGrane);

	cout << "Najbolja cena: " << minCena << endl;

	cout << "Najbolje grane: " << endl;

	for (int i = 0; i < graneLength; i++) {
		printf(" %c", (char)najboljeGrane[i] + 64);
		if ((i + 1) % 2 == 0 && i < 2 * k)
			cout << " - ";
	}
	cout << endl;

	return 0;
}