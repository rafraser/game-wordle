aws s3 cp "dist/index.html" "s3://rafraser-assets/game-wordle/index.html"
aws s3 cp "dist/main.js" "s3://rafraser-assets/game-wordle/main.js"
aws s3 sync "dist/assets" "s3://rafraser-assets/game-wordle/assets/"