use regex::Regex;
use std::fs;

pub struct Num {
    start: usize,
    end: usize,
    value: String,
}

pub struct Sym {
    pos: usize,
    value: String,
}

pub struct Line {
    nums: Vec<Num>,
    syms: Vec<Sym>,
}

fn parse_lines(input: &str) -> Vec<Line> {
    let re_int = Regex::new(r#"[0-9]+"#).unwrap();
    let re_sym = Regex::new(r#"[^A-Za-z0-9\.]"#).unwrap();
    let mut parsed_lines: Vec<Line> = Vec::new();
    for line in input.lines() {
        let ints: Vec<Num> = re_int
            .find_iter(line)
            .map(|x| Num {
                value: x.as_str().to_string(),
                start: x.start(),
                end: x.end() - 1, // end returns the next byte for some reason
            })
            .collect();
        let syms: Vec<Sym> = re_sym
            .find_iter(line)
            .map(|x| Sym {
                value: x.as_str().to_string(),
                pos: x.start(),
            })
            .collect();
        parsed_lines.push(Line {
            nums: ints,
            syms: syms,
        });
    }
    return parsed_lines;
}

fn is_adjacent(num: &Num, sym: &Sym) -> bool {
    // first condition to avoid doing usize 0 - 1 that is overflow
    if num.start == 0 {
        if sym.pos <= (num.end + 1) {
            return true;
        } else {
            return false;
        }
    }
    if (sym.pos >= (num.start - 1)) && (sym.pos <= (num.end + 1)) {
        return true;
    }
    return false;
}

fn check_line(num: &Num, line: &Line) -> i32 {
    let mut sum: i32 = 0;
    for sym in line.syms.iter() {
        if is_adjacent(num, sym) {
            sum += num.value.parse::<i32>().unwrap();
        }
    }
    return sum;
}

fn check_gear(sym: &Sym, line: &Line) -> Vec<i32> {
    let mut gear: Vec<i32> = Vec::new();
    for num in line.nums.iter() {
        if is_adjacent(num, sym) {
            gear.push(num.value.parse::<i32>().unwrap());
        }
    }
    return gear;
}

fn part_1(lines: &Vec<Line>) {
    let mut sum = 0;
    // for number of each line in the file look if there are some
    // symbols in the previous, current and next line that are adjacent
    for (i, line) in lines.iter().enumerate() {
        let prev;
        if i != usize::MIN {
            prev = lines.get(i - 1);
        } else {
            prev = None;
        }
        let next = lines.get(i + 1);
        for num in line.nums.iter() {
            if prev.is_some() {
                sum += check_line(num, prev.unwrap());
            }
            sum += check_line(num, line);
            if next.is_some() {
                sum += check_line(num, next.unwrap());
            }
        }
    }
    println!("The sum of the part numbers is {}", sum);
}

fn part_2(lines: &Vec<Line>) {
    let mut sum: i32 = 0;
    for (i, line) in lines.iter().enumerate() {
        let prev;
        if i != usize::MIN {
            prev = lines.get(i - 1);
        } else {
            prev = None;
        }
        let next = lines.get(i + 1);
        for sym in line.syms.iter().filter(|x| x.value == "*") {
            let mut maybe_gear: Vec<i32> = Vec::new();
            if prev.is_some() {
                maybe_gear.append(&mut check_gear(sym, prev.unwrap()));
            }
            maybe_gear.append(&mut check_gear(sym, line));

            if next.is_some() {
                maybe_gear.append(&mut check_gear(sym, next.unwrap()));
            }
            if maybe_gear.len() == 2 {
                sum += maybe_gear[0] * maybe_gear[1];
            }
        }
    }

    println!("The sum of the gear ratios is {}", sum);
}

fn main() {
    let input: String = fs::read_to_string("/home/skylake/aoc2023/inputs/3.txt").unwrap();
    let lines = parse_lines(&input);
    part_1(&lines);
    part_2(&lines);
}
