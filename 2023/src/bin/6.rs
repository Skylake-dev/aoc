use regex::Regex;
use std::fs;

fn get_ints(re: &Regex, text: &str) -> Vec<u64> {
    return re
        .find_iter(text)
        .map(|m| m.as_str())
        .map(|i| i.parse::<u64>().unwrap())
        .collect();
}

fn get_single_int(re: &Regex, text: &str) -> u64 {
    return re
        .find_iter(text)
        .map(|m| m.as_str())
        .collect::<Vec<&str>>()
        .join("")
        .parse::<u64>()
        .unwrap();
}

fn compute_ways(target: &u64, time: &u64) -> u64 {
    let mut ways = 1;
    for hold_for in 0..*time {
        let speed = hold_for;
        let move_for = time - hold_for;
        if move_for * speed > *target {
            ways += 1;
        }
    }
    return ways - 1;
}

fn part_1(input: &String) {
    let int = Regex::new(r#"[0-9]+"#).unwrap();
    let lines: Vec<&str> = input.split("\n").collect();
    let times = get_ints(&int, lines[0]);
    let distances = get_ints(&int, lines[1]);
    let mut all_ways: u64 = 1;
    let len = times.len();
    for i in 0..len {
        let target = distances.get(i).unwrap();
        let time = times.get(i).unwrap();
        all_ways *= compute_ways(target, time);
    }
    println!("[part1] Total ways are: {}", all_ways);
}

fn part_2(input: &String) {
    let int = Regex::new(r#"[0-9]+"#).unwrap();
    let lines: Vec<&str> = input.split("\n").collect();
    let time = get_single_int(&int, lines[0]);
    let target = get_single_int(&int, lines[1]);
    println!("[part2] Total ways are: {}", compute_ways(&target, &time));
}

fn main() {
    let input: String = fs::read_to_string("/home/skylake/aoc2023/inputs/6.txt").unwrap();
    part_1(&input);
    part_2(&input);
}
