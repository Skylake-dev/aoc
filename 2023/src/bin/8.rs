use regex::Regex;
use std::{collections::HashMap, fs};

pub struct Link<'a> {
    left: &'a str,
    right: &'a str,
}

fn parse_input(input: &String) -> (&str, HashMap<&str, Link>) {
    let mut lines = input.lines();
    let mut nodes: HashMap<&str, Link> = HashMap::new();
    let instructions: &str;
    let re = Regex::new(r#"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)"#).unwrap();
    instructions = lines.next().unwrap();
    lines.next(); // ignores empty line
    for line in lines {
        let labels = re.captures(line).unwrap();
        let label = labels.get(1).unwrap().as_str();
        let left = labels.get(2).unwrap().as_str();
        let right = labels.get(3).unwrap().as_str();
        nodes.insert(
            label,
            Link {
                left: left,
                right: right,
            },
        );
        println!("{}", line);
    }
    return (instructions, nodes);
}

fn follow_path(
    instructions: &str,
    nodes: &HashMap<&str, Link>,
    start: &str,
    is_target: fn(&str) -> bool,
) -> u64 {
    let mut end = false;
    let mut steps = 0;
    let mut instr = instructions.chars();
    let mut current_instruction;
    let mut current_node = nodes.get(start).unwrap();
    let mut next_label;
    while !end {
        current_instruction = instr.next();
        match current_instruction {
            None => {
                // restart the instruction
                instr = instructions.chars();
                current_instruction = instr.next();
            }
            _ => {}
        }
        steps += 1;
        if current_instruction.unwrap() == 'R' {
            next_label = current_node.right;
        } else {
            next_label = current_node.left;
        }
        if is_target(next_label) {
            end = true;
        } else {
            current_node = nodes.get(next_label).unwrap();
        }
    }
    return steps;
}

fn part_1(instructions: &str, nodes: &HashMap<&str, Link>) {
    let steps = follow_path(instructions, nodes, "AAA", |x| x == "ZZZ");
    println!("[part1] The number of steps is {}", steps);
}

fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 {
        return a;
    }
    return gcd(b, a % b);
}

fn lcm(a: u64, b: u64) -> u64 {
    return (a / gcd(a, b)) * b;
}

fn part_2(instructions: &str, nodes: &HashMap<&str, Link>) {
    let mut steps = Vec::new();
    let starting_nodes: Vec<&str> = nodes
        .keys()
        .filter(|x| x.ends_with("A"))
        .map(|x| *x) //i don't get it
        .collect::<Vec<&str>>();
    for node in starting_nodes {
        steps.push(follow_path(instructions, nodes, node, |x| x.ends_with("Z")));
    }
    let total = steps.iter().map(|x| *x).reduce(|a, b| lcm(a, b)).unwrap();
    println!("[part2] The number of steps is {}", total);
}

fn main() {
    let input: String = fs::read_to_string("/home/skylake/aoc2023/inputs/8.txt").unwrap();
    let (instructions, nodes) = parse_input(&input);
    part_1(instructions, &nodes);
    part_2(instructions, &nodes);
}
