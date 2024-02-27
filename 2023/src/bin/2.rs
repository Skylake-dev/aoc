use regex::Regex;
use std::fs;

pub struct Game {
    game_id: i32,
    possible: bool,
    red: Vec<i32>,
    green: Vec<i32>,
    blue: Vec<i32>,
}

// returns 0 if no match
fn get_one_i32_from_regex(re: &Regex, text: &str) -> i32 {
    let num = re.captures(text);
    match num {
        Some(i) => {
            return i.get(1).unwrap().as_str().parse::<i32>().unwrap();
        }
        _ => {
            return 0;
        }
    }
}

// this is very stupid because i build the regex every time
fn parse_game(line: &str) -> Game {
    let game_id = Regex::new(r#"Game ([0-9]+):"#).unwrap();
    let rounds = line.split(";");
    let red = Regex::new(r#"([0-9]+) red"#).unwrap();
    let green = Regex::new(r#"([0-9]+) green"#).unwrap();
    let blue = Regex::new(r#"([0-9]+) blue"#).unwrap();
    // can i use the line number to get game id? yes, thank you for your concern, but i like this
    let id = get_one_i32_from_regex(&game_id, line);
    let mut game = Game {
        game_id: id,
        possible: false,
        red: Vec::new(),
        green: Vec::new(),
        blue: Vec::new(),
    };
    for round in rounds {
        game.red.push(get_one_i32_from_regex(&red, round));
        game.green.push(get_one_i32_from_regex(&green, round));
        game.blue.push(get_one_i32_from_regex(&blue, round));
    }
    return game;
}

fn part_1(input: &String) {
    const RED_THRESHOLD: i32 = 12;
    const GREEN_THRESHOLD: i32 = 13;
    const BLUE_THRESHOLD: i32 = 14;
    let mut games: Vec<Game> = vec![];
    for line in input.lines() {
        let mut game = parse_game(line);
        if (game.red.iter().max().unwrap() > &RED_THRESHOLD)
            || (game.green.iter().max().unwrap() > &GREEN_THRESHOLD)
            || (game.blue.iter().max().unwrap() > &BLUE_THRESHOLD)
        {
            game.possible = false;
        } else {
            game.possible = true;
        }
        games.push(game);
    }
    let sum: i32 = games.iter().filter(|x| x.possible).map(|x| x.game_id).sum();
    println!("Sum of all possible game ids: {}", sum);
}

fn part_2(input: &String) {
    let mut power: Vec<i32> = Vec::new();
    for line in input.lines() {
        let game = parse_game(line);
        // max value for each color and multiply together
        power.push(
            game.red.iter().max().unwrap()
                * game.green.iter().max().unwrap()
                * game.blue.iter().max().unwrap(),
        );
    }
    let sum: i32 = power.iter().sum();
    println!("Sum of all power: {}", sum);
    let oneliner: i32 = input
        .lines()
        .map(|x| parse_game(x))
        .map(|x| {
            x.red.iter().max().unwrap()
                * x.green.iter().max().unwrap()
                * x.blue.iter().max().unwrap()
        })
        .sum();
    println!("Sum of all power: {}", oneliner);
}

fn main() {
    let input: String = fs::read_to_string("/home/skylake/aoc2023/inputs/2.txt").unwrap();
    part_1(&input);
    part_2(&input);
}
