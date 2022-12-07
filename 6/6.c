#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define INPUT_LEN 4096 + 1
#define PRESENT 1
#define NOT_PRESENT 0
#define FAIL -1

int is_present(char* marker, char element, int marker_len) {
    for (int i = 0; i < marker_len; i++) {
        if (element == *(marker + i))
            return PRESENT;
    }
    return NOT_PRESENT;
}

void insert(char* marker, char element, int first_free_cell) {
    *(marker + first_free_cell) = element;
}

int shift(char* marker, char shift_until, int first_free_cell) {
    int offset = 0;   // position of the duplicate char
    int shift_to = 0;
    while (*(marker + offset) != shift_until) {
        offset++;
    }
    offset++; // move to first character to shift
    while(offset < first_free_cell) {
        // from the next char, shift all back to the beginning
        *(marker + shift_to) = *(marker + offset);
        offset++;
        shift_to++;
    }
    return shift_to;
}

int find_marker(char* line, int pattern_len) {
    int marker_offset = 0;          // offset of the marker (start of marker + len(marker))
    int first_free_cell = 0;        // where i am in the marker now
    char curr_char;                 // what is the current char
    char marker[pattern_len + 1];   // keep track of possible markers of the specified length
    // initialize array to null
    for (int i = 0; i< pattern_len; i++) {
        marker[i] = '\0';
    }
    for (int i = 0; i < INPUT_LEN; i++) {
        marker_offset++;
        curr_char = *(line + i);
        if ((curr_char == '\n') || (curr_char == '\0')) {
            break;
        }
        if (is_present(marker, curr_char, first_free_cell) == NOT_PRESENT) {
            insert(marker, curr_char, first_free_cell);
            first_free_cell++;
            if (first_free_cell == pattern_len) {
                //found the marker
                puts(marker);
                return marker_offset;
            }
        } else {
            first_free_cell = shift(marker, curr_char, first_free_cell);
            insert(marker, curr_char, first_free_cell);
            first_free_cell++;
        }
    }
    puts("failed to find marker\n");
    exit(FAIL);
}

void main() {
    FILE *data;
    char line[INPUT_LEN];
    int packet_marker_offset, message_marker_offset;
    data = fopen("./input", "r");
    assert(data != NULL);
    // file is composed of a single line
    fgets(line, INPUT_LEN, data);
    fclose(data);
    packet_marker_offset = find_marker(line, 4);
    message_marker_offset = find_marker(line, 14);
    printf("packet offset: %d\nmessage offset: %d\n", packet_marker_offset, message_marker_offset);
}