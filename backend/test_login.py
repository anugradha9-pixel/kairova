 from app.auth.security import verify_password

hash1 = "$bcrypt-sha256$v=2,t=2b,r=12$WpNkeGZWVdFDu1VYFl770.$hdoEXNAiZNjKO9o.2DYKWg4v2ltopzS"
hash2 = "$bcrypt-sha256$v=2,t=2b,r=12$FZrJXVwNITEY22GpodP8iO$HvhcW0emZlHY6EH5S2RYf1wpjigVZFW"

print("user1:", verify_password("securepass123", hash1))
print("user2:", verify_password("securepass123", hash2)) 