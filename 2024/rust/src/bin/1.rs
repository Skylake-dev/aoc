use std::collections::HashMap;
use std::fs;
use std::iter::zip;

fn parse_input(input: &String) -> (Vec<i32>, Vec<i32>) {
    let mut left: Vec<i32> = Vec::new();
    let mut right: Vec<i32> = Vec::new();
    // split lines on the spaces and parse the integers
    for line in input.lines() {
        let ints = line
            .split("   ")
            .map(|i| i.parse::<i32>().unwrap())
            .collect::<Vec<i32>>();
        left.push(ints[0]);
        right.push(ints[1])
    }
    // keep lists sorted for ease of use
    left.sort();
    right.sort();
    return (left, right);
}

fn part_1(left: &Vec<i32>, right: &Vec<i32>) {
    // compute the absolute difference between the two elements and sum
    let result: i32 = zip(left, right)
        .into_iter()
        .map(|(l, r)| (l - r).abs())
        .sum();
    println!("part 1: {result}");
}

fn part_2(left: &Vec<i32>, right: &Vec<i32>) {
    // count the number of elements in the right list
    let mut counts: HashMap<i32, i32> = HashMap::new();
    for el in right {
        // should be equivalent to *counts.entry(el).or_insert(0) += 1
        counts.entry(*el).and_modify(|c| *c += 1).or_insert(1);
    }
    let similarity_score = left
        .iter()
        .map(|num| num * counts.get(num).unwrap_or(&0)) // i don't understand why i should borrow 0
        .sum::<i32>();
    println!("part 1: {similarity_score}");
}

fn main() {
    let input: String = fs::read_to_string("../../../inputs/1.txt").unwrap();
    let (left, right) = parse_input(&input);
    part_1(&left, &right);
    part_2(&left, &right);
}
