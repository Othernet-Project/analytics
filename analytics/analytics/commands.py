from .tasks import process_stats


def stats_from_file(arg, supervisor):
    print('Begin stats import from: {}'.format(arg))
    try:
        with open(arg, 'r') as stats_file:
            data = stats_file.read()
    except Exception:
        print('Cannot open stats file: {}'.format(arg))
    else:
        process_stats(supervisor, data)
        print('Stat import finished.')
    finally:
        raise supervisor.EarlyExit()
