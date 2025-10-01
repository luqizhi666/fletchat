from supabase import create_client, Client

# url = "https://ossjaxuoahrjnqopbzen.supabase.co"
url = "https://supabase.022408.xyz"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zc2pheHVvYWhyam5xb3BiemVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3ODc4NDMsImV4cCI6MjA3MTM2Mzg0M30.hhr57_wbhM6_-4Z63vPugliQb-i3Fg4J90HGT7okEZY"  # 用户端用 anon key

supabase: Client = create_client(url, key)
response = supabase.auth.sign_in_with_password(
    {"email": "test@example.com", "password": "password"}
)
print(response)
print(response.user.id)


response = (
    supabase.table("users")
    .upsert({"id": response.user.id , "username": "new_username", "email": response.user.email, "avatar_url": "https://example.com/new.jpg", "status": "offline"})
    .execute()
)
# email还是可以直接被用户修改，所以这里是自定义邮箱显示
print(response)