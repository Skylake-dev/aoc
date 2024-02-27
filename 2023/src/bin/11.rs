use std::fs;

pub struct Galaxy {
    x: i64,
    y: i64,
}

fn parse_input(input: &String, expansion_factor: i64) -> Vec<Galaxy> {
    let mut galaxies: Vec<Galaxy> = Vec::new();
    let mut y_expansion = 0;
    for (y, line) in input.lines().enumerate() {
        if !line.contains("#") {
            y_expansion += expansion_factor - 1; // *100 means that i add the 99 remaining lines (100 - 1)
        } else {
            for (x, _) in line.match_indices("#") {
                galaxies.push(Galaxy {
                    x: x as i64,
                    y: (y as i64) + y_expansion,
                });
            }
        }
    }
    // find the empty columns
    let mut xs: Vec<i64> = galaxies.iter().map(|g| g.x).collect();
    xs.sort_unstable();
    xs.dedup();
    // start from right to avoid moving a galaxy too much
    for i in (*xs.iter().min().unwrap()..*xs.iter().max().unwrap()).rev() {
        if !xs.contains(&i) {
            // move right all galaxies
            for g in galaxies.iter_mut() {
                if g.x > i {
                    g.x += expansion_factor - 1;
                }
            }
        }
    }
    return galaxies;
}

fn compute_distance(g1: &Galaxy, g2: &Galaxy) -> i64 {
    return (g1.x - g2.x).abs() + (g1.y - g2.y).abs();
}

fn shortest_paths(galaxies: &Vec<Galaxy>) -> i64 {
    let mut sum = 0;
    for (i, g1) in galaxies.iter().enumerate() {
        let mut distances = Vec::new();
        for g2 in galaxies[i + 1..].iter() {
            distances.push(compute_distance(g1, g2));
        }
        sum += distances.iter().sum::<i64>();
    }
    return sum;
}

fn part_1(input: &String) {
    let galaxies = parse_input(input, 2);
    let sum = shortest_paths(&galaxies);
    println!("The sum of the minimum distances is {sum}");
}

fn part_2(input: &String) {
    let galaxies = parse_input(input, 1000000);
    let sum = shortest_paths(&galaxies);
    println!("The sum of the minimum distances is {sum}");
}

fn main() {
    let input: String = fs::read_to_string("/home/skylake/aoc2023/inputs/11.txt").unwrap();
    part_1(&input);
    part_2(&input);
}
