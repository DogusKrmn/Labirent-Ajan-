# Labirent-Ajan-

Pygame ile yazılmış, 20x50 hücrelik bir labirentte BFS algoritmasıyla beraber yapılmış bir en kısa yolu bulma projesi.
Özellikler
Kullanıcılar labirente istediği gibi duvarlar ekleyip silebilir ve değişiklik yapabilir.
BFS'in taradığı kareler animasyonla gösterilir
Hedefe ulaşıldığında bulunan en kısa yolu çizme ve adım sayısını yazma
Yol bulunamazsa uyarı verme

BFS nasıl çalışır?

BFS, başlangıç noktasından başlayıp önce en yakın karelere, sonra onların komşularına doğru dalga dalga yayılır. Bir kuyruk (deque) kullanır: kuyruğun başından bir kare alır, gidilebilir komşularını kuyruğun sonuna ekler. Her kareyi hangi kareden gelerek keşfettiğini (ata sözlüğü) kaydeder. Hedefe ulaşınca bu kayıtlar hedeften geriye doğru izlenerek yol çıkarılır.

<img width="1243" height="612" alt="image" src="https://github.com/user-attachments/assets/6b5ed7b1-854b-4caa-a607-e29336523bc0" />
