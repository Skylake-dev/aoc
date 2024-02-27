use std::{cmp::Ordering, collections::HashMap, fs};

#[derive(PartialEq, PartialOrd, Eq, Debug)]
pub enum Type {
    HighCard = 0,
    OnePair = 1,
    TwoPair = 2,
    ThreeOfAKind = 3,
    FullHouse = 4,
    FourOfAKind = 5,
    FiveOfAKind = 6,
}

#[derive(PartialEq, PartialOrd, Eq, Debug)]
pub struct Hand {
    raw_cards: Vec<u32>,
    cards: Vec<u32>, // ensure this is sorted in descending order
    value: Type,
    bet: u32,
}

impl Ord for Hand {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.value > other.value {
            return Ordering::Greater;
        } else if self.value < other.value {
            return Ordering::Less;
        } else {
            for i in 0..self.raw_cards.len() {
                if self.raw_cards[i] > other.raw_cards[i] {
                    return Ordering::Greater;
                } else if self.raw_cards[i] < other.raw_cards[i] {
                    return Ordering::Less;
                }
            }
            // this state is impossible
            let x = false;
            assert!(x);
            return Ordering::Equal;
        }
    }
}

fn map_strength(c: char) -> u32 {
    let strength: HashMap<char, u32> = HashMap::from([
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
        ('6', 6),
        ('7', 7),
        ('8', 8),
        ('9', 9),
        ('T', 10),
        ('J', 11),
        ('Q', 12),
        ('K', 13),
        ('A', 14),
    ]);
    return strength[&c];
}

fn map_type(cards: &Vec<u32>) -> Type {
    let mut counts = cards.clone();
    counts.dedup();
    let case = counts.len();
    match case {
        5 => {
            return Type::HighCard;
        }
        4 => {
            return Type::OnePair;
        }
        3 => {
            if (cards[0] == cards[2]) || (cards[1] == cards[3]) || (cards[2] == cards[4]) {
                return Type::ThreeOfAKind;
            }
            return Type::TwoPair;
        }
        2 => {
            if (cards[0] == cards[3]) || (cards[1] == cards[4]) {
                return Type::FourOfAKind;
            }
            return Type::FullHouse;
        }
        1 => {
            return Type::FiveOfAKind;
        }
        _ => {
            return Type::HighCard;
        }
    }
}

// already sorted by rank
fn parse_input(input: &String) -> Vec<Hand> {
    let mut hands: Vec<Hand> = Vec::new();
    for line in input.lines() {
        let parts: Vec<&str> = line.split(" ").collect();
        assert_eq!(parts.len(), 2);
        let bet = parts[1].parse::<u32>().unwrap();
        let raw_cards = parts[0]
            .chars()
            .map(|c| map_strength(c))
            .collect::<Vec<u32>>();
        let mut cards: Vec<u32> = raw_cards.clone();
        cards.sort();
        cards.reverse();
        let value = map_type(&cards);
        let card = Hand {
            raw_cards: raw_cards,
            cards: cards,
            value: value,
            bet: bet,
        };
        hands.push(card);
    }
    hands.sort_unstable_by(|a, b| a.cmp(b));
    return hands;
}

fn part_1(hands: &Vec<Hand>) {
    let sum: usize = hands
        .iter()
        .enumerate()
        .map(|x| (x.0 + 1) * x.1.bet as usize)
        .sum();
    println!("[part1] The total winnings are {}", sum);
}

fn main() {
    let input: String = fs::read_to_string("/home/skylake/aoc2023/inputs/7.txt").unwrap();
    let hands = parse_input(&input);
    part_1(&hands);
}
