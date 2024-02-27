use std::{collections::HashMap, fs};

pub struct Lens<'a> {
    label: &'a str,
    focal_len: u32,
}

fn hash(step: &str) -> u32 {
    let mut current_value: u32 = 0;
    const MUL: u32 = 17;
    for ch in step.chars() {
        assert!(ch.is_ascii());
        current_value += ch as u32;
        current_value *= MUL;
        current_value %= 256;
    }
    return current_value;
}

fn part_1(input: &String) {
    let sum: u32 = input.split(",").map(|s| hash(s)).sum();
    println!("The sum of the initializations sequences is {sum}");
}

fn part_2(input: &String) {
    let sequence = input.split(",");
    let mut sum = 0;
    let mut boxes: HashMap<u32, Vec<Lens>> = HashMap::new();
    for step in sequence {
        let instruction: Vec<&str> = step.split(&['=', '-'][..]).collect();
        let label = instruction[0];
        let h = hash(label);
        if instruction.len() == 2 && instruction[1] != "" {
            // the symbol was =
            let focal_len = instruction[1].parse::<u32>().unwrap();
            // search for the box
            let content = boxes.get_mut(&h);
            match content {
                // there is something in the box
                Some(x) => {
                    let el = x.iter().position(|l| l.label == label);
                    match el {
                        // the label is already present, replace focal len
                        Some(y) => {
                            x[y].focal_len = focal_len;
                        }
                        // new label, push lens to the back
                        None => {
                            x.push(Lens {
                                label: label,
                                focal_len: focal_len,
                            });
                        }
                    }
                }
                // no box, create and insert it
                None => {
                    let mut v = Vec::new();
                    v.push(Lens {
                        label: label,
                        focal_len: focal_len,
                    });
                    boxes.insert(h, v);
                }
            }
        } else {
            // the symbol was -
            let content = boxes.get_mut(&h);
            match content {
                // there is something in the box
                Some(x) => {
                    let el = x.iter().position(|l| l.label == label);
                    match el {
                        // the label is already present, remove it
                        Some(y) => {
                            x.remove(y);
                        }
                        // not present, don't care
                        _ => {}
                    }
                }
                // no box, don't care
                _ => {}
            }
        }
    }
    // now do the sum
    for (i, lens) in boxes.iter() {
        let box_value = i + 1;
        for (j, l) in lens.iter().enumerate() {
            sum += box_value * ((j as u32) + 1) * l.focal_len;
        }
    }
    println!("The sum of the focal power is {sum}");
}

fn main() {
    println!("Remove newline from your input before running");
    let input: String = fs::read_to_string("/home/skylake/aoc2023/inputs/15.txt").unwrap();
    part_1(&input);
    part_2(&input);
}
