from blog_parser import main

from datetime import datetime


if __name__ == "__main__":
    start = datetime.now()
    main()
    end = datetime.now()
    print('This run took {} seconds'.format((end-start).total_seconds()))

