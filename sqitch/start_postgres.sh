set -e

until psql -h mypgdb -p 5432 --username sqitch -d lexicount -c '\l'; do
  >&2 echo "DB is unavailable - sleeping"
  sleep 1
done

cd /sqitch
sqitch deploy db:postgres://sqitch@mypgdb:5432/lexicount
