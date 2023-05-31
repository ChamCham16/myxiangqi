import subprocess, time
import threading
from typing import List, Dict

pikafish_lock = threading.Lock()

def get_best_move(moves: str, think_time: int):

    pikafish_lock.acquire()

    try:
        pikafish_path = './Pikafish/pikafish.exe'
        pikafish = subprocess.Popen(
            pikafish_path,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=1,
        )

        try:
            pikafish.stdin.write('ucinewgame\n')
            pikafish.stdin.flush()

            position_command = 'position startpos moves {}\n'.format(moves)
            pikafish.stdin.write(position_command)
            pikafish.stdin.flush()

            if think_time == 0:
                pikafish.stdin.write('go depth 16\n')
                pikafish.stdin.flush()
            else:
                pikafish.stdin.write('go movetime {}\n'.format(think_time))
                pikafish.stdin.flush()

            infos: List[str] = []
            best_move = None
            ponder = None

            while True:
                output_line = pikafish.stdout.readline().strip()
                if output_line.startswith('bestmove'):
                    print('best move found!')
                    parts = output_line.split(' ')
                    if len(parts) > 1:
                        best_move = parts[1]
                    if len(parts) > 3:
                        ponder = parts[3]

                    break
                if output_line.startswith('info depth'):
                    infos.append(output_line)

            pikafish.stdin.write('quit\n')
            pikafish.stdin.flush()

            return best_move, ponder, parse_info_lines(infos)
        
        except:
            pikafish.terminate()
            raise

    finally:
        pikafish_lock.release()

def parse_info_line(info_line: str):
    result = {}

    info_line = info_line.replace('lowerbound nodes', 'nodes')
    info_line = info_line.replace('upperbound nodes', 'nodes')
    info_line = info_line.replace('info ', '')
    info_line = info_line.replace('score ', '')

    info = info_line.split(' pv ')[0]
    result['pv'] = info_line.split(' pv ')[1]

    info_parts = info.split(' ')

    for i in range(0, len(info_parts), 2):
        key = info_parts[i]
        value = info_parts[i+1]

        result[key] = value

    return result

def parse_info_lines(info_lines: List[str]):
    parsed_info_lines = [parse_info_line(line) for line in info_lines]

    max_depth: str = max(parsed_info_lines, key=lambda x : int(x['depth']))['depth']

    filtered_lines = [line for line in parsed_info_lines if line['depth'] == max_depth]

    if len(filtered_lines) > 1:
        max_score: str = max(filtered_lines, key=lambda x : int(x['cp']))['cp']

        filtered_lines = [line for line in filtered_lines if line['cp'] == max_score]

    return filtered_lines[0]