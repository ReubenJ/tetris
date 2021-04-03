//! Actions taken within a game of Tetris.
//! 
//! These functions are all actions which the Tetris game must be
//! able to execute in order to run the game. All functions are pure
//! taking some combination of 2D [Vec](std::vec::Vec)s


/// Rotates a shape clockwise
/// ```
/// # use tetris::actions::rotate_clockwise;
/// let before = vec![
///     vec![1, 1, 1],
///     vec![0, 1, 0],
/// ];
/// 
/// let actual = rotate_clockwise(before);
/// 
/// let expect = vec![
///     vec![0, 1],
///     vec![1, 1],
///     vec![0, 1]
/// ];
/// 
/// assert_eq!(expect, actual);
/// ```
pub fn rotate_clockwise(shape: Vec<Vec<i8>>) -> Vec<Vec<i8>> {
    let mut ret: Vec<Vec<i8>> = Vec::new();

    for x in 0..shape[0].len() {
        let mut row: Vec<i8> = Vec::new();
        for y in (0..shape.len()).rev() {
            row.push(shape[y][x])
        }
        ret.push(row)
    }
    ret
}

// pub fn check_collision(board: &Vec<Vec<i8>>, shape: &Vec<i8>, offset: (i8, i8)) {

// }

// pub fn remove_row(board: Vec<Vec<i8>>, row: i8) -> Vec<Vec<i8>> {
//     board
// }

// pub fn join_matrices(mat1: Vec<Vec<i8>>, mat2: Vec<i8>, mat2_offset: (i8, i8)) -> Vec<Vec<i8>> {
//     mat1
// }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rotate_l_shape() {
        let before = vec![
            vec![1, 1, 1],
            vec![0, 0, 1],
        ];

        let actual = rotate_clockwise(before);

        let expect = vec![
            vec![0, 1],
            vec![0, 1],
            vec![1, 1]
        ];

        assert_eq!(expect, actual, "Expected {:?}, got {:?}", expect, actual);
    }

    #[test]
    fn rotate_o_shape() {
        let before = vec![
            vec![7, 7],
            vec![7, 7],
        ];

        let actual = rotate_clockwise(before);

        let expect = vec![
            vec![7, 7],
            vec![7, 7],
        ];

        assert_eq!(expect, actual, "Expected {:?}, got {:?}", expect, actual);
    }

    #[test]
    fn rotate_i_shape() {
        let before = vec![
            vec![6, 6, 6, 6],
        ];

        let actual = rotate_clockwise(before);

        let expect = vec![
            vec![6],
            vec![6],
            vec![6],
            vec![6],
        ];

        assert_eq!(expect, actual, "Expected {:?}, got {:?}", expect, actual);
    }

    #[test]
    fn rotate_i_shape_twice() {
        let before = vec![
            vec![6, 6, 6, 6],
        ];

        let actual = rotate_clockwise(rotate_clockwise(before.to_vec()));

        assert_eq!(before, actual, "Expected {:?}, got {:?}", before, actual);
    }
}