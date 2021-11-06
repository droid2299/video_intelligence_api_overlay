import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Video Intelligence API Logo Detection and OD/OT')

    parser.add_argument(
            '--gcp_uri',
            type=str,
            default='test_bucket/cut.mp4',
            help='''
                GCP Bucket URI to the input video file to be processed''')

    parser.add_argument(
            '--type',
            type=str,
            default='logo_detection',
            help='''
                Type of detection required: logo_detection or od_ot''')

    parser.add_argument(
            '--save_results_txt',
            type=str,
            default='results.txt',
            help='''
                Path to save the bbox coordinates, coodrinates, time_offset and confidence in a txt file''')


    parser.add_argument(
            '--min_confidence',
            type=float,
            default=0.7,
            help='''
                Minimum Confidence for overlaying on videos''')

    parser.add_argument(
            '--language_code',
            type=str,
            default='en',
            help='''
                Language used in the video file''')


    
    return parser.parse_args()

