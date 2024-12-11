import argparse
def linkedin_args_parser():
    """
    Main function to handle LinkedIn automation.

    This function uses argparse to parse command-line arguments for LinkedIn automation.
    It supports sending connection requests, liking posts, and commenting on posts.
    It also allows setting limits for each action.

    Parameters:
    -s, --send-connections: A flag to indicate whether to send connection requests on LinkedIn.
    -l, --like-posts: A flag to indicate whether to like LinkedIn posts.
    -c, --comment-posts: A flag to indicate whether to comment on LinkedIn posts.
    --connection-limit: An integer specifying the limit for sending connection requests. Default is 10.
    --like-scroll-limit: An integer specifying the scroll limit for liking posts. Default is 5.
    --comment-scroll-limit: An integer specifying the scroll limit for commenting on posts. Default is 2.

    Returns:
    args: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="LinkedIn Automation Tool")
    parser.add_argument(
        "-s", "--send-connections", 
        help="Send connection requests on LinkedIn", 
        action="store_true"
    )
    parser.add_argument(
        "-l", "--like-posts", 
        help="Like LinkedIn posts", 
        action="store_true"
    )
    parser.add_argument(
        "-c", "--comment-posts", 
        help="Comment on LinkedIn posts", 
        action="store_true"
    )
    parser.add_argument(
        "--connection-limit", 
        type=int, 
        default=10, 
        help="Limit for sending connection requests (default: 10)"
    )
    parser.add_argument(
        "--like-scroll-limit", 
        type=int, 
        default=5, 
        help="Scroll limit for liking posts (default: 5)"
    )
    parser.add_argument(
        "--comment-scroll-limit", 
        type=int, 
        default=2, 
        help="Scroll limit for commenting on posts (default: 2)"
    )

    args = parser.parse_args()

    return args
