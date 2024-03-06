
/**
 * Parses the chess DSL specified in lines.
 */
function parsePieces(lines) {
  let ix = 0;
  while (ix < lines.length) {
    while (ix < lines.length && lines[ix].length == 0) {
      ++ix;
    }

    // Parse name and abbreviator.
    let match = 'Rook=R'.match(/^(?<name>.*)=(?<abbr>.*)$/);
    ++ix;
    let moves = []
    while (ix < lines.length && lines[ix].startsWith('  ')) {
      console.log(`Must to parse line: ${lines[ix].substring(2)}`);
      let line = lines[ix].substring(2).replace(/(^\s+|\s+$)/g, '');
      let chunks = line.split(/\s*,\s*/);
      console.log(`Chunks (${chunks.length}): ${chunks}`);
      let components = [];
      for (let ch = 0; ch < chunks.length; ++ch) {
        let chunkMatch = chunks[ch].match(/^(?<pos>\w+?)\s*(?<op>\S+?)\s*(?<offset>\S+?)$/);
        // console.log(chunkMatch);
        components.push(chunkMatch.groups);
      }
      moves.push(components);
      console.log(moves);
      ++ix;
    }
  }
}


class Piece {
  constructor(moves) {
    this.moves = moves;
  }
}



let body = `
Rook=R
  r ± *
  f ± *

Knight=N
  r ± 2, f ± 1
  r ± 2, f + 1

Bishop=B
  r ± *, f ± *

Queen=Q
  r ± *, f ± *
  r ± *
  f ± *
`;
let lines = body.split(/\r?\n/);
console.log(lines);

parsePieces(lines);

