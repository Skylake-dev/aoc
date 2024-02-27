use std::{collections::HashMap, fs, vec};

fn part_1(lines: &String) {
    let digits: Vec<char> = vec!['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'];
    let mut numbers: Vec<i32> = Vec::new();
    for line in lines.split("\n") {
        // indicates if found one digit
        let mut flag = false;
        let mut first: Option<char> = None;
        let mut last: Option<char> = None;
        let mut string_number: String = String::new();
        for ch in line.chars() {
            if digits.contains(&ch) {
                if flag {
                    last = Some(ch);
                } else {
                    first = Some(ch);
                    flag = true;
                }
            }
        }
        match (first, last) {
            (Some(x), Some(y)) => {
                string_number.push(x);
                string_number.push(y);
            }
            (Some(x), None) => {
                string_number.push(x);
                string_number.push(x);
            }
            _ => {
                string_number.push('0');
            }
        }

        numbers.push(string_number.parse::<i32>().unwrap());
    }
    let sum: i32 = numbers.iter().sum();
    println!("[part 1] The sum is {}", sum);
}

fn map_index(matches: &Vec<&str>, value: &str) -> char {
    let translation: HashMap<&str, char> = HashMap::from([
        ("one", '1'),
        ("two", '2'),
        ("three", '3'),
        ("four", '4'),
        ("five", '5'),
        ("six", '6'),
        ("seven", '7'),
        ("eight", '8'),
        ("nine", '9'),
        ("zero", '0'),
    ]);
    let mut ch = '0';
    if translation.contains_key(value) {
        ch = translation.get(value).unwrap().clone(); // idk why this is needed need to learn rust lol
    } else if matches.contains(&value) {
        ch = value.chars().nth(0).unwrap();
    }
    return ch;
}

fn part_2(lines: &String) {
    let matches: Vec<&str> = vec![
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "one", "two", "three", "four", "five",
        "six", "seven", "eight", "nine", "zero",
    ];
    let mut numbers: Vec<i32> = Vec::new();
    // define type for collection value
    #[derive(Debug)]
    pub struct StrIndex<'a> {
        pub number: &'a str,
        pub first_index: Option<usize>,
        pub last_index: Option<usize>,
    }
    for line in lines.split("\n") {
        let mut string_number = String::new();
        let result = matches
            .iter()
            .map(|x| StrIndex {
                number: x,
                first_index: line.find(x),
                last_index: line.rfind(x),
            })
            .filter(|x| x.first_index != None)
            .collect::<Vec<StrIndex>>();
        // get the first (lowest index)
        let first_idx = result
            .iter()
            .min_by(|x, y| x.first_index.cmp(&y.first_index))
            .unwrap();
        // get the last (highest index)
        let last_idx = result
            .iter()
            .max_by(|x, y| x.last_index.cmp(&y.last_index))
            .unwrap();
        if first_idx.number == last_idx.number {
            // there is only one number on the line, duplicate
            string_number.push(map_index(&matches, first_idx.number));
            string_number.push(map_index(&matches, first_idx.number));
        } else {
            string_number.push(map_index(&matches, first_idx.number));
            string_number.push(map_index(&matches, last_idx.number));
        }
        numbers.push(string_number.parse::<i32>().unwrap());
    }
    let sum: i32 = numbers.iter().sum();
    println!("[part 2] The sum is {}", sum);
}

fn main() {
    let lines: String =
        fs::read_to_string("/home/skylake/aoc2023/inputs/1.txt").expect("non ho capito");
    part_1(&lines);
    part_2(&lines);
}
