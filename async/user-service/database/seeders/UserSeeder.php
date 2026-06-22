<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;
use App\Models\User;

class UserSeeder extends Seeder
{
    public function run()
    {
        // Tetap masukkan user admin untuk testing
        User::create([
            'name' => 'Admin User',
            'email' => 'admin@gmail.com',
            'password' => Hash::make('password123'),
        ]);

        // Generate 50 user random tambahan (tanpa Faker)
        for ($i = 0; $i < 50; $i++) {
            User::create([
                'name' => 'User ' . \Illuminate\Support\Str::random(5),
                'email' => \Illuminate\Support\Str::random(10) . '@example.com',
                'password' => Hash::make('password'),
            ]);
        }
    }
}
