use std::{env, fs, process};

fn get_range(line: &str) -> (u64, u64) {
    let x = line.split_once("-").unwrap();
    return (x.0.parse::<u64>().unwrap(), x.1.parse::<u64>().unwrap());
}

fn part_1(lines: &str) {
    let mut parse_range = true; // flag to switch from parsing ranges to parsing ingredients
    let mut ranges: Vec<(u64, u64)> = Vec::new();
    let mut fresh = 0;
    for line in lines.lines() {
        if line.len() == 0 {
            parse_range = false;
            continue;
        }
        match parse_range {
            true => {
                ranges.push(get_range(line));
            }
            false => {
                let ingredient = line.parse::<u64>().unwrap();
                // i have no idea why here the normal loop doesn't compile
                for (low, high) in ranges.iter() {
                    if ingredient >= *low && ingredient <= *high {
                        fresh += 1;
                        break;
                    }
                }
            }
        };
    }
    println!("[part 1]Fresh ingredients {fresh}");
}

fn part_2(lines: &str) {
    let mut ranges: Vec<(u64, u64)> = Vec::new();
    let mut fresh = 0;
    for line in lines.lines() {
        if line.len() == 0 {
            break;
        }
        ranges.push(get_range(line));
    }
    // sort all ranges accoording to their start
    // tuple are sorted correctly by comparing each value in order
    ranges.sort();
    // merge ranges together
    let mut merged_ranges: Vec<(u64, u64)> = Vec::new();
    let mut curr_start = ranges[0].0;
    let mut curr_end = ranges[0].1;
    for (low, high) in ranges[1..].iter() {
        // low is always greater or equal to curr_start since array is sorted
        if *low > curr_end {
            // this range doesn't overlap, end the current range and start new
            merged_ranges.push((curr_start, curr_end));
            curr_start = *low;
        }
        if *high > curr_end {
            curr_end = *high;
        }
    }
    // push last range
    merged_ranges.push((curr_start, curr_end));
    // count all possible fresh
    for (low, high) in merged_ranges.iter() {
        fresh += *high - *low + 1;
    }
    println!("[part 1]Fresh ingredients {fresh}");
}

static INPUT: &'static str = "./inputs/5.txt";
static TEST_INPUT: &'static str = "./inputs/5_test.txt";

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
