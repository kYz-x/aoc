use std::fs;
use std::env;


struct Grid {
    grid: Vec<Vec<char>>
}

struct Pos(usize,usize);

#[derive(Debug)]
enum Dir {
    Up,
    Down,
    Left,
    Right,
    Start,
}

impl Grid {

    fn new(content: Vec<Vec<char>>) -> Grid {
        Grid { grid: content }
    }

    /* Getting the Starting Position 'S' Location */
    fn get_s_pos(&self) -> Option<Pos> {
        for (j, row) in self.grid.iter().enumerate() {
            for (i, &char) in row.iter().enumerate() {
                if char == 'S' {return Some(Pos(i, j));}
            }
        }
        None
    }

    /* Check if starting to end position is a valid path */
    fn valid_path(&self, start: Pos, end: Pos) -> bool {
        let start_c = self.grid[start.1][start.0];
        let end_c   = self.grid[end.1][end.0];
        let dir;
        
        /* Finding Direction */
        if      end.0 > start.0 {dir = Dir::Right;}
        else if end.0 < start.0 {dir = Dir::Left;}
        else if end.1 > start.1 {dir = Dir::Down;}
        else if end.1 < start.1 {dir = Dir::Up;}
        else {
            panic!("Start and end position cannot be equal !");
        }
        
        match start_c {
            'S' => if matches!(dir, Dir::Up)    && (end_c == '7' || end_c == '|' || end_c == 'F') || 
                      matches!(dir, Dir::Down)  && (end_c == 'L' || end_c == '|' || end_c == 'J') ||  
                      matches!(dir, Dir::Left)  && (end_c == 'F' || end_c == '-' || end_c == 'L') ||  
                      matches!(dir, Dir::Right) && (end_c == '7' || end_c == '-' || end_c == 'J')
                      {true} else {false},
            
            '-' => if matches!(dir, Dir::Right) && (end_c == '7' || end_c == '-' || end_c == 'J') || 
                      matches!(dir, Dir::Left)  && (end_c == 'F' || end_c == '-' || end_c == 'L') 
                      {true} else {false},

            '|' => if matches!(dir, Dir::Up)    && (end_c == '7' || end_c == '|' || end_c == 'F') || 
                      matches!(dir, Dir::Down)  && (end_c == 'L' || end_c == '|' || end_c == 'J') 
                      {true} else {false},
                      
            'L' => if matches!(dir, Dir::Up)    && (end_c == '7' || end_c == '|' || end_c == 'F') || 
                      matches!(dir, Dir::Right) && (end_c == '7' || end_c == '-' || end_c == 'J') 
                      {true} else {false},
            
            'J' => if matches!(dir, Dir::Up)    && (end_c == '7' || end_c == '|' || end_c == 'F') || 
                      matches!(dir, Dir::Left)  && (end_c == 'F' || end_c == '-' || end_c == 'L') 
                      {true} else {false},

            '7' => if matches!(dir, Dir::Down)  && (end_c == 'J' || end_c == '|' || end_c == 'L') || 
                      matches!(dir, Dir::Left)  && (end_c == 'F' || end_c == '-' || end_c == 'L') 
                      {true} else {false},
            
            'F' => if matches!(dir, Dir::Right) && (end_c == 'J' || end_c == '-' || end_c == '7') || 
                      matches!(dir, Dir::Down)  && (end_c == 'J' || end_c == '|' || end_c == 'L') 
                      {true} else {false},

            _   => false,
        }
    }

    /* Find path length starting from pos and coming from dir */
    fn find_max_path(&mut self, path: Pos, dir: Dir) -> u32 { 
        let mut stack: Vec<(Pos, Dir, u32)> = Vec::new();
        let mut res1 : u32 = 0;

        stack.push((path, dir, 0));

        while !stack.is_empty()
        {
            let call = stack.pop().unwrap();
            let Pos (x,y) = call.0; 
            let dir = call.1;
            let val = call.2;

            /* Trying Right */
            if !matches!(dir, Dir::Right)  &&                     // if it doens't already come from the right
            x+1 < self.grid.len()          &&                     // if it doens't reach a boundary
            self.valid_path(Pos(x,y),Pos(x+1,y))                  // verify that the character (pipes) display a valid path
            {
                stack.push((Pos(x+1,y), Dir::Left, val+1));   // if good, then find the rest of the path length
            }

            /* Trying Left */
            if !matches!(dir, Dir::Left)  && 
            x > 0                         && 
            self.valid_path(Pos(x,y),Pos(x-1,y)) 
            {
                stack.push((Pos(x-1,y), Dir::Right, val+1));
            }

            /* Trying Down */
            if !matches!(dir, Dir::Down) && 
            y+1 < self.grid[0].len()     && 
            self.valid_path(Pos(x,y),Pos(x,y+1)) 
            {
                stack.push((Pos(x,y+1), Dir::Up, val+1));
            }

            /* Trying Up   */
            if !matches!(dir, Dir::Up)    && 
            y > 0                         && 
            self.valid_path(Pos(x,y),Pos(x,y-1)) 
            {
                stack.push((Pos(x,y-1), Dir::Down, val+1));
            }
            
            res1 = res1.max(val)
        }

        return res1;    // return the path with the maximum length (hoping that's the loop :p)
    }

}

fn main() {
    let args: Vec<String> = env::args().collect();

    /*** File Processing ***/
    let fname = &args[1];
    let contents = fs::read_to_string(fname).expect("erreur lors de l'ouverture du fichier {s}");
    let mut char_mat  : Vec<Vec<char>> = Vec::new();

    let lines = contents.split('\n');
    for line in lines {
        let line : Vec<char> = line.chars().collect();
        char_mat.push(line);
    }

    /*** Part 1 Implementation ***/
    let mut grid = Grid::new(char_mat);
    let s_pos = grid.get_s_pos().unwrap();
    let s_len = grid.find_max_path(s_pos, Dir::Start);
    let res1  = (s_len+1) / 2;

    // Printing Results
    println!("Number of step to halfway of the loop starting from S (Part 1): {:?}", res1);
}