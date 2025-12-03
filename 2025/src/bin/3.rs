use std::{env, fs, process};

fn get_highest_digit_but_leave_enough_to_complete(
    line: &str,              // line to examine
    start: usize,            // offset to start search from
    digits_remaining: usize, // digits to leave at the end to search for the next
) -> (usize, char) {
    // idea: get the highest digit while leaving enough digits to complete the number
    // this gives us the highest possible number
    let mut max_idx = 0;
    let mut digit = '0';
    // these are ascii strings so i can get away with normal indexing
    for (i, c) in line.char_indices() {
        // go to starting offset
        if i < start {
            continue;
        }
        // skip trailng part
        if i == line.len() - digits_remaining {
            break;
        }
        // get highest number
        if c > digit {
            max_idx = i;
            digit = c;
        }
    }
    // return the next starting point
    return (max_idx + 1, digit);
}

fn get_n_digits_higest_number(line: &str, number_of_digits: usize) -> u64 {
    let mut digits = Vec::new();
    let mut idx = 0;
    let mut digit: char;
    let mut digits_remaining = number_of_digits;
    while digits_remaining > 0 {
        digits_remaining -= 1;
        (idx, digit) = get_highest_digit_but_leave_enough_to_complete(line, idx, digits_remaining);
        digits.push(digit);
    }
    // add together
    return digits.iter().collect::<String>().parse::<u64>().unwrap();
}

fn part_1(lines: &str) {
    const DIGITS: usize = 2;
    let mut total_joltage = 0;
    for line in lines.lines() {
        total_joltage += get_n_digits_higest_number(line, DIGITS);
    }
    println!("[part 1]The password is {total_joltage}");
}

fn part_2(lines: &str) {
    const DIGITS: usize = 12;
    let mut total_joltage = 0;
    for line in lines.lines() {
        total_joltage += get_n_digits_higest_number(line, DIGITS);
    }
    println!("[part 2]The password is {total_joltage}");
}

static INPUT: &'static str = "./inputs/3.txt";
static TEST_INPUT: &'static str = "./inputs/3_test.txt";

fn main() {
    let args: Vec<String> = env::args().collect();
    let name: &str;
    if args.len() > 1 && args[1] == "test" {
        name = TEST_INPUT;
    } else {
        name = INPUT
    }
    let lines: String = match fs::read_to_string(name) {
        Ok(s) => s,
        Err(_) => {
            println!("There was an error when opening the input file");
            process::exit(-1);
        }
    };
    part_1(&lines);
    part_2(&lines);
}
