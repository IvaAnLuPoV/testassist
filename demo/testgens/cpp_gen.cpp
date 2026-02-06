#include "testlib.h"
#include <bits/stdc++.h>
using namespace std;

int main(int argc, char** argv){
    registerGen(argc, argv, 1);
    int n = opt<int>("n");
    int m = opt<int>("m");
    cout << n << " " << m << endl;
    for(int i = 0; i < n; i ++){
    	for(int j = 0; j < m; j ++){
    		cout << rnd.next(10) << " ";
    	} cout << endl;
    }
}

