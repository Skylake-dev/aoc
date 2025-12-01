use std::{env, fs, process};

// numbers on the dial
const DIAL_NUMS: i32 = 100;
const STARTING_NUM: i32 = 50;

fn get_sign_and_number(line: &str) -> (i32, i32) {
    // get the sign
    let sign = match line.chars().nth(0) {
        Some('L') => -1,
        Some('R') => 1,
        _ => panic!(),
    };
    // get the number, can get away with this since it is ascii
    // remember to trim \n or this will panic
    let number = match line.trim()[1..].parse::<i32>() {
        Ok(x) => x,
        Err(_) => panic!(),
    };
    return (sign, number);
}

fn part_1(lines: &str) {
    let mut sign; // whether the rotation is left or right
    let mut number; // temporary variable to hold line number
    let mut pointed_value: i32 = STARTING_NUM; // initial dial position
    let mut zero_counter: i32 = 0; // counts the number of times the dial is at 0
    for line in lines.split("\n").into_iter().filter(|x| x.len() > 0) {
        // parse the line
        (sign, number) = get_sign_and_number(line);
        // do the computation
        pointed_value = (pointed_value + (sign * number)).rem_euclid(DIAL_NUMS);
        // only count when the dial is at 0
        if pointed_value == 0 {
            zero_counter += 1;
        }
    }
    println!("[part 1]The password is {zero_counter}");
}

fn part_2(lines: &str) {
    let mut sign; // whether the rotation is left or right
    let mut number; // temporary variable to hold line number
    let mut previous_pointed_value: i32; // track the last value, to see if i crossed 0
    let mut pointed_value: i32 = STARTING_NUM; // initial dial position
    let mut zero_counter: i32 = 0; // counts the number of times the dial is at 0
    for line in lines.split("\n").into_iter().filter(|x| x.len() > 0) {
        // parse the line
        (sign, number) = get_sign_and_number(line);
        // instead of considering only the final value count every time
        // the dial passes through zero
        // first add the number of complete rotations
        zero_counter += number / DIAL_NUMS;
        // then check if the remaining part of the rotation passes through zero
        previous_pointed_value = pointed_value;
        pointed_value = (pointed_value + sign * number).rem_euclid(DIAL_NUMS);
        // see all possible cases
        if pointed_value == 0 // dial stopped at 0
            || sign < 0 && pointed_value > previous_pointed_value && previous_pointed_value != 0
            || sign > 0 && pointed_value < previous_pointed_value && previous_pointed_value != 0
        {
            zero_counter += 1;
        }
    }
    println!("[part 2]The password is {zero_counter}");
}

static INPUT: &'static str = "./inputs/1.txt";
static TEST_INPUT: &'static str = "./inputs/1_test.txt";

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
