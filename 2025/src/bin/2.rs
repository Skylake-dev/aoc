use std::{env, fs, process};

fn get_tuples(lines: &str) -> Vec<(u64, u64)> {
    // panic on malformed input
    return lines
        .split(",")
        .map(|x| x.split_once("-").unwrap())
        .map(|x| (x.0.parse::<u64>().unwrap(), x.1.parse::<u64>().unwrap()))
        .collect();
}

fn exponent_for_modulo_or_zero(n: u64) -> u32 {
    // closest power of 10 lower than the number
    let exp = n.ilog10();
    if exp % 2 == 0 {
        // odd number of digits, cannot be split in two sequences
        // remember 10^2 (even exponent) = 100 (odd digits)
        return 0;
    }
    // exp + 1 is surely even
    return (exp + 1) / 2;
}

fn get_bounds_and_modulo_exponent(low: u64, high: u64) -> (u64, u64, u32) {
    // return the bounds for the search, as well as the exponent to use
    let mut exp_low = exponent_for_modulo_or_zero(low);
    let mut exp_high = exponent_for_modulo_or_zero(high);
    // get upper and lower bound for ranges excluding numbers that
    // have odd number of digits
    let (lower, upper) = match (exp_low, exp_high) {
        (0, 0) => return (0, 0, 0), // all numbers have odd digits, skip
        (0, _) => {
            // only second part has even digits
            exp_low = exp_high;
            (10_u64.pow(exp_high * 2 - 1), high)
        }
        (_, 0) => {
            // only fist part has even digits
            exp_high = exp_low;
            (low, 10_u64.pow(exp_low * 2))
        }
        (_, _) => (low, high), // whole range has even number of digits
    };
    return (lower, upper, exp_low);
}

fn find_repeated_twice_in_range(lower: u64, upper: u64, exp: u32) -> u64 {
    // return th sum of the numbers that respect the condition
    // of being two repeated sequence of numbers e.g. 11, 123123, etc
    let mut count: u64 = 0;
    let module = 10_u64.pow(exp);
    for num in lower..upper + 1 {
        // check if lower half of the digits is the same as the upper half
        if num % module == num / module {
            count += num;
        }
    }
    return count;
}

fn part_1(lines: &str) {
    // assumption: each range can only span one order of magnitude
    // i.e 0 < high-low < 100
    let tuples = get_tuples(lines);
    let mut sum: u64 = 0;
    for (low, high) in tuples {
        // here exp is half the number of digits
        let (lower, upper, exp) = get_bounds_and_modulo_exponent(low, high);
        if (lower, upper, exp) == (0, 0, 0) {
            continue; // this means that no number needs to be checked here
        }
        // if the assumption is correct, i only have a single range to check
        sum += find_repeated_twice_in_range(lower, upper, exp);
    }
    println!("[part1] The sum is {sum}");
}

fn part_2(lines: &str) {}

static INPUT: &'static str = "./inputs/2.txt";
static TEST_INPUT: &'static str = "./inputs/2_test.txt";

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
    println!("{:?}", get_tuples(&lines));
    part_1(&lines);
    part_2(&lines);
}
