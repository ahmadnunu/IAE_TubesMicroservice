<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Faker\Factory as Faker;

class OrderSeeder extends Seeder
{
    public function run(): void
    {
        $statuses = ['pending', 'processing', 'completed', 'cancelled'];
        
        for ($i = 0; $i < 50; $i++) {
            DB::table('orders')->insert([
                'user_id' => rand(1, 50),
                'product_id' => rand(1, 50),
                'quantity' => rand(1, 5),
                'total_price' => rand(15, 200) * 1000,
                'status' => $statuses[array_rand($statuses)],
                'order_date' => now()->subDays(rand(1, 30)),
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
    }
}
