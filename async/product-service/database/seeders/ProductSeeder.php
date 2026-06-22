<?php
namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Product;

class ProductSeeder extends Seeder
{
    public function run()
    {
        $products = [
            ['name' => 'Sushi', 'description' => 'Nasi gulung dengan ikan mentah dan rumput laut', 'price' => 28000, 'stock' => 20],
            ['name' => 'Ramen', 'description' => 'Mi kuah khas Jepang dengan kaldu gurih', 'price' => 32000, 'stock' => 15],
            ['name' => 'Tempura', 'description' => 'Udang goreng tepung renyah', 'price' => 25000, 'stock' => 18],
            ['name' => 'Okonomiyaki', 'description' => 'Pancake gurih berisi kol dan topping', 'price' => 27000, 'stock' => 10],
            ['name' => 'Takoyaki', 'description' => 'Bola-bola gurita dengan saus manis-asin', 'price' => 20000, 'stock' => 25],
        ];

        foreach ($products as $product) {
            Product::create($product);
        }

        // Generate 35 additional random products tanpa Faker
        $adjectives = ['Enak', 'Pedas', 'Manis', 'Spesial', 'Premium', 'Super', 'Jumbo'];
        for ($i = 0; $i < 35; $i++) {
            Product::create([
                'name' => 'Makanan ' . $adjectives[array_rand($adjectives)] . ' ' . rand(1, 100),
                'description' => 'Deskripsi produk random ' . \Illuminate\Support\Str::random(10),
                'price' => rand(10, 100) * 1000,
                'stock' => rand(5, 100)
            ]);
        }
    }
}
