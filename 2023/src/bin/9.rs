use std::fs;

fn parse_input(input: &String) -> Vec<Vec<i32>> {
    let mut sequences = Vec::new();
    for line in input.lines() {
        let seq = line
            .split(" ")
            .map(|i| i.parse::<i32>().unwrap())
            .collect::<Vec<i32>>();
        sequences.push(seq);
    }
    return sequences;
}

fn do_diff(seq: Vec<i32>) -> Vec<i32> {
    let mut diff: Vec<i32> = Vec::new();
    for i in 0..(seq.len() - 1) {
        diff.push(seq[i + 1] - seq[i]);
    }
    return diff;
}

fn part_1(sequences: &Vec<Vec<i32>>) {
    let mut last_el: Vec<i32> = Vec::new();
    for seq in sequences {
        let mut last_diff: Vec<i32> = Vec::new();
        last_diff.push(*(seq.last().unwrap()));
        let mut end: bool = false;
        let mut diff = seq.clone();
        while !end {
            diff = do_diff(diff);
            last_diff.push(*(diff.last().unwrap()));
            if diff.iter().all(|x| *x == 0) {
                end = true;
            }
        }
        last_el.push(last_diff.iter().sum());
    }
    println!(
        "[part1] The sum of all the last elements is {}",
        last_el.iter().sum::<i32>()
    );
}

fn part_2(sequences: &Vec<Vec<i32>>) {
    let mut first_el: Vec<i32> = Vec::new();
    for seq in sequences {
        let mut first_diff: Vec<i32> = Vec::new();
        first_diff.push(seq[0]);
        let mut end: bool = false;
        let mut diff = seq.clone();
        while !end {
            diff = do_diff(diff);
            first_diff.push(diff[0]);
            if diff.iter().all(|x| *x == 0) {
                end = true;
            }
        }
        first_el.push(
            first_diff
                .iter()
                .rev()
                .map(|x| *x)
                .reduce(|x, y| y - x)
                .unwrap(),
        );
    }
    println!(
        "[part2] The sum of all the first elements is {}",
        first_el.iter().sum::<i32>()
    );
}

fn main() {
    let input: String = fs::read_to_string("/home/skylake/aoc2023/inputs/9.txt").unwrap();
    let sequences = parse_input(&input);
    part_1(&sequences);
    part_2(&sequences);
}
