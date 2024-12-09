import React from "react";
import { Layout } from "../app/layout";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ResumeUploadForm } from "@/components/ResumeUploadForm";
import { ResumeDetails } from "@/components/ResumeDetails";

export const Dashboard: React.FC = () => {
  return (
    <Layout>
      <div className="mt-5 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-xl bg-white p-6 shadow-lg dark:bg-navy-800">
          {/* <div className="grid w-full max-w-sm items-center gap-1.5">
            <Label htmlFor="picture">Picture</Label>
            <Input id="picture" type="file" />
          </div> */}
          <ResumeUploadForm />
        </div>
      </div>
    </Layout>
  );
};

