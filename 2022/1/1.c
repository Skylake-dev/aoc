#include <stdio.h>
#include <stdlib.h>
#include <assert.h>



void adjust_top3(int top3[3], int curr_value) {
    if (curr_value > top3[0]) {
        top3[1] = top3[0];
        top3[2] = top3[1];
        top3[0] = curr_value;
    }
    else if (curr_value > top3[1]) {
        top3[2] = top3[1];
        top3[1] = curr_value;
    }
    else if (curr_value > top3[2]) {
        top3[2] = curr_value;
    }
}


void main() {
    //open input data
    FILE *data;
    data = fopen("./input", "r");
    assert(data != NULL);
    char raw[20];
    int curr_value = 0;
    int top3[3] = {0, 0, 0};

    while(fgets(raw, 20, data) != NULL) {
        if (raw[1] == '\n') {  //newlines are \r\n
            //keep track of current top3 and start over
            adjust_top3(top3, curr_value);
            curr_value = 0;
        } 
        else {
            //parse int from string and add to current value
            int tmp;
            tmp = strtol(raw, NULL, 10);
            curr_value += tmp;
        }
    }

    printf("%d, %d, %d, total: %d\n", top3[0], top3[1], top3[2], top3[0] + top3[1] + top3[2]);
    //close the file
    fclose(data);
}