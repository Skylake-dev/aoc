use std::fs;

#[derive(Default)]
pub struct Connection {
    available: bool,
    connected: bool,
}

#[derive(Default)]

pub struct Pipe {
    label: char,
    up: Connection,
    down: Connection,
    left: Connection,
    right: Connection,
}

// parse in 2 steps, first get pipes then make connections
fn parse_input(input: &String) -> Vec<Vec<Pipe>> {
    let pipes = Vec::new();
    for line in input.lines() {
        let pipe_line: Vec<Pipe> = Vec::new();
        for c in line.chars() {
            match c {
                _ => {}
            }
        }
    }
    return pipes;
}

fn part_1(pipes: &Vec<Vec<Pipe>>) {}

fn part_2(pipes: &Vec<Vec<Pipe>>) {}

fn main() {
    let input: String = fs::read_to_string("/home/skylake/aoc2023/inputs/10.txt").unwrap();
    let pipes = parse_input(&input);
    part_1(&pipes);
    part_2(&pipes);
}
