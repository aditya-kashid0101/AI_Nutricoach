export type User = {
  id: number;
  name: string;
  email: string;
  created_at: string;
};

export type Profile = {
  id?: number;
  user_id?: number;
  age: number;
  gender: string;
  height_cm: number;
  weight_kg: number;
  fitness_goal: string;
  activity_level: string;
};

export type Nutrition = {
  bmr: number;
  tdee: number;
  activity_multiplier: number;
  calorie_target: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
  goal: string;
  explanation: string;
};

export type Food = {
  id: number;
  name: string;
  category: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  serving_g: number;
  vegetarian: boolean;
};

export type Intake = {
  id: number;
  food_id: number;
  food_name: string;
  servings: number;
  meal_type: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
};

export type Recommendation = {
  source: string;
  recommendation: string;
};
