# yes I know I probably shouldn't hardcode all this stuff
# no I don't care
aws s3 cp "dist/index.html" "s3://rafraser-assets/game-wordle/index.html"
aws s3 cp "dist/main.js" "s3://rafraser-assets/game-wordle/main.js"
aws s3 sync "dist/assets" "s3://rafraser-assets/game-wordle/assets/"

aws cloudfront create-invalidation --distribution-id "E3D33ZNMKGV48K" --paths "/index.html" "/main.js" "/assets/game_titles.json"